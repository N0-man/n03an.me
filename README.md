# n03an.me

My personal site with some hand-picked notes in Markdown and Jupyter notebooks, converted to HTML and served via GitHub Pages at https://n03an.me. nothing fancy...

```shell
pyenv install -l | less
pyenv install 3.12.4

# Activate Python 3.12 for the current project
pyenv local 3.12.4
source ~/.zshrc

# create venv and activate
python -m venv env
source env/bin/activate

# install dependencies
pip install -r requirements.txt
```

---

### Rendering base64 image attachments in JupiterBook

> **Note**: as of July2024, jupiter-book wasnt cleanly able to convert base64 image attachments from notebook cells into external image to be used within html. The program [extract_base64_attachments.py](/extract_base64_attachments.py) runs as part of the pipeline scan each notebook cells and extract base64 images into external image files. Once the images are extracted, `sphinx` would take care of isolating all the image files into single image director as part of `jupiter-book build`

---
### add scroll output 
if you dont want super long output html, add this metada to code output in text editor mode
```
   "metadata": {
    "tags": [
     "scroll-output"
    ]
   },
```