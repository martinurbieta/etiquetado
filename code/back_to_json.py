from PIL import Image
import cv2
import io
import base64
from skimage import measure
import imageio
import numpy as np
import json

im = "E010-MUN-01.jpg"
mask = "E010-MUN-01.png"
file_name = "E010-MUN-01.jpg"

mask = imageio.imread(mask)
mask = np.asarray(mask)
mask = mask.sum(-1)

def img_arr_to_b64(filename):
    img_arr = cv2.imread(filename)
    img_pil = Image.fromarray(img_arr)
    f = io.BytesIO()
    img_pil.save(f, format='JPEG')
    img_bin = f.getvalue()
    if hasattr(base64, 'encodebytes'):
        img_b64 = base64.encodebytes(img_bin)
    else:
           img_b64 = base64.encodestring(img_bin)
    return img_b64


annotation = {
    "lineColor": [0, 255, 0, 128],
    "shapes": [{"points": [], "line_color": None, "fill_color": None, "label": "xx"}],
    "imagePath": file_name,
    "imageData": img_arr_to_b64(im),
    "fillColor": [255, 0, 0, 128]
}

img = cv2.imread("E010-MUN-01.png", cv2.IMREAD_UNCHANGED)

img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#set a thresh
thresh = 100
#get threshold image
ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

#contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = measure.find_contours(thresh_img, 0.5)
contours = sorted(contours, key=len, reverse=True)[:1]
#print(contours)
for n, contour in enumerate(contours):
    #print(contour)
    coords = measure.approximate_polygon(contour, tolerance=3)[:-1]
    #print(coords)
    segmentation = np.flip(coords, axis=1).tolist()
    #print(segmentation)
    annotation["shapes"][0]["points"] = segmentation

file = file_name.replace(".jpg", ".json")
with open(file, 'w', encoding='utf8') as outfile:
    print(annotation)
    json.dump(annotation, outfile, indent=2, ensure_ascii=False)
