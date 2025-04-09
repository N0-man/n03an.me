import json
import sys
import os
from binascii import a2b_base64
import random
import string
import shutil
import glob

def generate_random_string(length=15):
    """Generate a random string of fixed length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# only for single notebook conversion via commandline
def validate_input_nb():
    if (sys.argv[1] is None):
        print('Please provide a file path')
        sys.exit()
    return sys.argv[1]

def get_input_notebook_path():
    """Validate and return the input notebook path from command line arguments."""
    try:
        input_path = sys.argv[1]
    except IndexError:
        print('Please provide a file path')
        sys.exit(1)
    return input_path

def create_attachment_folder(source_notebook):
    """Create a directory for attachments. Clean it if it already exists before creation."""
    attachment_folder = f"{source_notebook.split('.')[0]}_attachments"
    if os.path.exists(attachment_folder):
        shutil.rmtree(attachment_folder)
    os.makedirs(attachment_folder)
    return attachment_folder

def write_image(attachment_folder, data, name):
    image_name = f"{generate_random_string(10)}_{name}"
    image_file_path = os.path.join(attachment_folder, image_name)
    with open(image_file_path, 'wb') as img:
        img.write(data)
    return image_name

def replace_attachment_references(cell, nb_name, attachment_folder, image_name):
    """Replace attachment references in notebook cell with new file path."""
    # We only need the basename to embed within notebook
    attachment_folder_name = os.path.basename(attachment_folder).replace(" ", "%20")
    attach_str = "attachment:"+nb_name
    if any(attach_str in source_line for source_line in cell['source']):
        # Replace the attachment string in each line of the cell source
        cell['source'] = [source_line.replace(attach_str, f"{attachment_folder_name}/{image_name}") for source_line in cell['source']]
        cell["attachments"] = {} # Remove the base64 attachment from the cell

def process_attachments(nb, attachment_folder):
    for cell in nb['cells']:
        for name, attach in cell.get("attachments", {}).items():
            for mime, data in attach.items():
                # Binary files are base64-encoded, SVG is already XML
                if mime in {'image/png', 'image/jpeg', 'application/pdf'}:
                    # data is b64-encoded as text (str, unicode),
                    # we want the original bytes
                    data = a2b_base64(data)
                else:
                    data = data.encode("UTF-8")

                image_name = write_image(attachment_folder, data, name)
                replace_attachment_references(cell, name, attachment_folder, image_name)

def override_notebook(nb, output_file_path):
    with open(output_file_path, 'w') as output_file:
        json.dump(nb, output_file, indent=4)


# Only for individual notebook path via command line
# def main():
#     source_notebook = validate_input_nb()
#     attachment_folder = create_attachment_folder(source_notebook)

#     with open(source_notebook) as f:
#         nb = json.load(f)

#     process_attachments(nb, attachment_folder)
#     override_notebook(nb, source_notebook)

def main():
    start_path = '.'
    # Use glob.glob with the recursive flag set to True to find all .ipynb files
    for notebook_path in glob.glob(os.path.join(start_path, '**/*.ipynb'), recursive=True):
        # notebook_path will contain the path to a .ipynb file
        source_notebook = notebook_path[2:]
        print(f'Processing: {source_notebook}')
        attachment_folder = create_attachment_folder(source_notebook)

        with open(source_notebook) as f:
            nb = json.load(f)

        process_attachments(nb, attachment_folder)
        override_notebook(nb, source_notebook)

if __name__ == "__main__":
    main()