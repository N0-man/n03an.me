## Analysis on SigLIP probability

- Why low score (4%) on Umbrella text search given 1920×1080 image where umbrella is not the primary subject and small
- Why score improves to 99 when on the crop (328 × 308) image where umbrella is the primary object

### **1. Global image embeddings dilute small objects**

Models like **google/siglip-so400m-patch14-384** produce a **single embedding** for the _entire image_.
That embedding reflects all salient features in the frame, _weighted by their visual prominence_.

If the white umbrella is only:

- **tiny**
- **on the far right**
- **surrounded by much larger objects (people, buildings, scene context)**

…then the umbrella contributes almost nothing to the final pooled feature vector.

Your similarity search ends up comparing the text _“white umbrella”_ to an embedding dominated by _everything except the umbrella_, which is why you get **~4% similarity**.

### **2. Cropping makes the umbrella the dominant signal**

When you crop around the umbrella (328×308):

- the model’s attention is **forced to focus on the umbrella**
- the pooled embedding is now _mostly about the umbrella_
- similarity to the “white umbrella” text embedding shoots up → **~99%**

This is exactly what you would expect from global-pooling architectures.

### **3. SigLIP uses patch-level features + global pooling**

SigLIP divides the image into 14×14 pixel patches (because you’re using the 384 model).
Features from all patches are averaged (or projected) into one embedding.

So if the umbrella occupies, say:

- only **1–2%** of the image area → only ~1–2% of the patches contain umbrella features
  → umbrella signal is nearly lost after pooling.

This is an inherent limitation of all CLIP-style models.

### **4. Text embeddings capture the _concept_, not the tiny visual cue**

The text “white umbrella” is:

- unambiguous
- high-contrast conceptually
- strongly represented in the text encoder

When you compare that to a global embedding with only a faint trace of “umbrella,” similarity is low.

### **5. Why small-object detection is hard for embedding models**

These models:

- are pretrained for contrastive _image-level_ alignment
- are **not detectors**
- are **not trained to highlight small or rare objects in a cluttered scene**
