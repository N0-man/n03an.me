# Import necessary GStreamer libraries and DeepStream python bindings
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib
from common.bus_call import bus_call
import pyds

# Declaring class label ids, which should align with the deep learning neural network output labels
PGIE_CLASS_ID_CAR=0
PGIE_CLASS_ID_BICYCLE=1
PGIE_CLASS_ID_PERSON=2
PGIE_CLASS_ID_ROAD_SIGN=3

class_labels={
    PGIE_CLASS_ID_CAR: 'car',
    PGIE_CLASS_ID_BICYCLE: 'bicycle', 
    PGIE_CLASS_ID_PERSON: 'person', 
    PGIE_CLASS_ID_ROAD_SIGN: 'road sign'
}

obj_counts=[]

def build_simple_pipeline(input_source): 
    # Create GStreamer elements
    # Create Pipeline element that will form a connection of other elements
    pipeline=Gst.Pipeline()
    print("Created Pipeline")

    # Create Source element for reading from a file and set the location property
    source=Gst.ElementFactory.make("filesrc", "file-source")
    source.set_property('location', input_source)

    # Create H264 Parser with h264parse as the input file is an elementary h264 stream
    h264parser=Gst.ElementFactory.make("h264parse", "h264-parser")

    # Create Decoder with nvv4l2decoder for accelerated decoding on GPU
    decoder=Gst.ElementFactory.make("nvv4l2decoder", "nvv4l2-decoder")

    # Create Streamux with nvstreammux to form batches for one or more sources and set properties
    streammux=Gst.ElementFactory.make("nvstreammux", "stream-muxer")
    streammux.set_property('width', 888) 
    streammux.set_property('height', 696) 
    streammux.set_property('batch-size', 1)

    # Create Primary GStreamer Inference Element with nvinfer to run inference on the decoder's output after batching
    pgie=Gst.ElementFactory.make("nvinfer", "primary-inference")
    pgie.set_property('config-file-path', '/dli/task/spec_files/pgie_config_trafficcamnet_03.txt')
    
    sgie=Gst.ElementFactory.make("nvinfer", "secondary-inference")
    sgie.set_property('config-file-path', '/dli/task/spec_files/sgie_config_vehicletypenet_04.txt')

    # Create Convertor to convert from YUV to RGBA as required by nvdsosd
    nvvidconv1=Gst.ElementFactory.make("nvvideoconvert", "convertor1")

    # Create OSD with nvdsosd to draw on the converted RGBA buffer
    nvosd=Gst.ElementFactory.make("nvdsosd", "onscreendisplay")

    # Create Convertor to convert from RGBA to I420 as required by encoder
    nvvidconv2=Gst.ElementFactory.make("nvvideoconvert", "convertor2")

    # Create Capsfilter to enforce frame image format
    capsfilter=Gst.ElementFactory.make("capsfilter", "capsfilter")
    caps=Gst.Caps.from_string("video/x-raw, format=I420")
    capsfilter.set_property("caps", caps)

    # Create Encoder to encode I420 formatted frames using the MPEG4 codec
    encoder=Gst.ElementFactory.make("avenc_mpeg4", "encoder")
    encoder.set_property("bitrate", 2000000)

    # Create Sink with fakesink as the end point of the pipeline
    sink=Gst.ElementFactory.make('filesink', 'filesink')
    sink.set_property('location', 'output_04_raw.mpeg4')
    sink.set_property("sync", 1)
    print('Created elements')
    
    # Add elements to pipeline
    pipeline.add(source)
    pipeline.add(h264parser)
    pipeline.add(decoder)
    pipeline.add(streammux)
    pipeline.add(pgie)
    pipeline.add(sgie)
    pipeline.add(nvvidconv1)
    pipeline.add(nvosd)
    pipeline.add(nvvidconv2)
    pipeline.add(capsfilter)
    pipeline.add(encoder)
    pipeline.add(sink)
    print('Added elements to pipeline')

    # Link elements in the pipeline
    # filesrc -> h264parse -> nvv4l2decoder -> nvstreammux -> nvinfer -> fakesink
    source.link(h264parser)
    h264parser.link(decoder)

    # Link decoder source pad to streammux sink pad
    decoder_srcpad=decoder.get_static_pad("src")    
    streammux_sinkpad=streammux.get_request_pad("sink_0")
    decoder_srcpad.link(streammux_sinkpad)

    # Link the rest of the elements in the pipeline
    streammux.link(pgie)
    pgie.link(sgie)
    sgie.link(nvvidconv1)
    nvvidconv1.link(nvosd)
    nvosd.link(nvvidconv2)
    nvvidconv2.link(capsfilter)
    capsfilter.link(encoder)
    encoder.link(sink)
    print('Linked elements in pipeline')
    
    return pipeline

def pgie_src_pad_buffer_probe(pad, info):
    """
    Callback function that iterates through metadata and prints out the details of the objects detected

    Args: 
        pad
        info

    Returns: 
        Gst.PadProbeReturn.OK
    """
    gst_buffer=info.get_buffer()

    # Retrieve batch metadata from the gst_buffer
    # Note that pyds.gst_buffer_get_nvds_batch_meta() expects the
    # C address of gst_buffer as input, which is obtained with hash(gst_buffer)
    batch_meta=pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame=batch_meta.frame_meta_list
    
    # Iterate through each frame in the batch metadata until the end
    while l_frame is not None:
        try:
            frame_meta=pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        frame_num=frame_meta.frame_num
        num_obj=frame_meta.num_obj_meta
        l_obj=frame_meta.obj_meta_list
        
        print("Frame Number={} Number of Objects={}".format(frame_num, num_obj))
        
        # Append number of objects a list 
        obj_counts.append(num_obj)
        
        # Iterate through each object in the frame metadata until the end
        while l_obj is not None:
            try:
                obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
                print('\t Object: {} - Top: {}, Left: {}, Width: {}, Height: {}'.format(obj_meta.obj_label, \
                                                                                        round(obj_meta.rect_params.top), \
                                                                                        round(obj_meta.rect_params.left), \
                                                                                        round(obj_meta.rect_params.width), \
                                                                                        round(obj_meta.rect_params.height)))
            except StopIteration:
                break
            
            try: 
                l_obj=l_obj.next
            except StopIteration:
                break
        
        try:
            l_frame=l_frame.next
        except StopIteration:
            break
    return Gst.PadProbeReturn.OK

def osd_sink_pad_buffer_probe(pad, info):
    gst_buffer = info.get_buffer()

    # Retrieve batch metadata from the gst_buffer
    # Note that pyds.gst_buffer_get_nvds_batch_meta() expects the
    # C address of gst_buffer as input, which is obtained with hash(gst_buffer)
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list

    # Iterate through each frame in the batch metadata until the end
    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        frame_num=frame_meta.frame_num
        num_obj = frame_meta.num_obj_meta
        l_obj=frame_meta.obj_meta_list
        
        print("Frame Number={} Number of Objects={}".format(frame_num, num_obj))
        
        # Iterate through each object in the frame metadata until the end
        while l_obj is not None:
            try:
                obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
                
                # Define an analyze_meta function to manipulate metadata
                analyze_meta(obj_meta)
            except StopIteration:
                break
                
            try: 
                l_obj=l_obj.next
            except StopIteration:
                break
        
        try:
            l_frame=l_frame.next
        except StopIteration:
            break
    return Gst.PadProbeReturn.OK

# Define helper function
def analyze_meta(obj_meta): 
    # Only car supports secondary inference
    if obj_meta.class_id == PGIE_CLASS_ID_CAR:     
        cls_meta=obj_meta.classifier_meta_list
        
        # Iterate through each class meta until the end
        while cls_meta is not None:
            cls=pyds.NvDsClassifierMeta.cast(cls_meta.data)
            # Get label info
            label_info=cls.label_info_list  
            
            # Iterate through each label info meta until the end
            while label_info is not None:
                # Cast data type of label from pyds.GList
                label_meta=pyds.glist_get_nvds_label_info(label_info.data)
                if cls.unique_component_id==2:
                    print('\t Type & Probability = {}% {}'.format(round(label_meta.result_prob*100), label_meta.result_label))
                try:
                    label_info=label_info.next
                except StopIteration:
                    break
            
            try:
                cls_meta=cls_meta.next
            except StopIteration:
                break
    return None

def main(args):
    # Check input arguments
    if len(args) != 2:
        sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
        sys.exit(1)

    # Standard GStreamer initialization
    Gst.init(None)
    
    pipeline=build_simple_pipeline(args[1])
    
    # Get the nvinfer plugin by name
    # sgie=pipeline.get_by_name('secondary-inference')
    nvosd=pipeline.get_by_name('onscreendisplay')
    
    # Add probe to inference plugin's source
    osdsinkpad = nvosd.get_static_pad("sink")
    osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe)
    print('Attached probe')
    
    # Create an event loop
    loop=GLib.MainLoop()
    
    # Feed GStreamer bus mesages to it
    bus=pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
    print('Added bus message handler')

    # Start play back and listen to events
    print("Starting pipeline")
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except:
        pass
    
    # Cleaning up as the pipeline comes to an end
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
