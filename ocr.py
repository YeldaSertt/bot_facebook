"""This code converts images to text and extracts data with regex."""
import io
import os
import re
from PIL import Image
import pytesseract
from wand.image import Image as wi
import pandas as pd

PATH = os.listdir('OC/')
HASHLIST = []
TEMPLIST = []
OUTPUT = {}

for u in PATH:
    hash_url = u.split("_")[-2]
    HASHLIST.append(hash_url)
    pdf = wi(filename=f"OC/{u}", resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    if hash_url not in OUTPUT:
        OUTPUT[hash_url] = []

    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))
    im = Image.open(io.BytesIO(imageBlobs[0]))
    text = pytesseract.image_to_string(im, lang='tur')
    js = {}
    share = re.findall(r"(\d+) Paylaşım", text)
    if share:
        js["Paylaşım"] = "".join(share)

    else:
        js["Paylaşım"] = "0"
    comment = re.findall(r"(\d+) Yorum", text)
    if comment:
        js["Yorum"] = "".join(comment)
    else:
        js["Yorum"] = "0"

    js["text"] = text
    OUTPUT[hash_url].append(js)
for out in OUTPUT:
    for image_text in OUTPUT[out]:
        with open(f'{out}.txt', "a") as f:
            f.write(image_text["text"] + "\n")

        del image_text["text"]

    df = pd.DataFrame(OUTPUT[out])
    df.to_csv(f'OC/bot-facebook_{out}.csv', index=False)

