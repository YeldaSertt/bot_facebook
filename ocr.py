"""This code converts images to text and extracts data with regex."""
import os
import re
from PIL import Image
import pytesseract as pt
import pandas as pd
PATH = "OCR"
TEMPLIST = []
for imageName in os.listdir(PATH):
    inputPath = os.path.join(PATH, imageName)
    img = Image.open(inputPath)
    text = pt.image_to_string(img, lang="tur")
    imagePath = imageName.split("_")[-2]
    fullTempPath = os.path.join('bot-facebook'+imagePath+".txt")
    js = {}
    share = re.findall(r"(\d+) Paylaşım", text)
    if share:
        js["Paylaşım"] = "".join(share)
        print(("".join(text)).split(js["Paylaşım"])[0])
    else:
        js["Paylaşım"] = "0"
    comment = re.findall(r"(\d+) Yorum", text)
    if comment:
        js["Yorum"] = "".join(comment)
    else:
        js["Yorum"] = "0"
    TEMPLIST.append(js)
    df = pd.DataFrame(TEMPLIST)
    df.to_csv(f'OCR/bot-facebook_{imagePath}.csv', index=False)
    file1 = open(fullTempPath, "w")
    file1.write(text)
    file1.close()
