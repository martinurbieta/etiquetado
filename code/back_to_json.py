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
contours = measure.find_contours(mask, 0.5)
contours = sorted(contours, key=len, reverse=True)[:1]
for n, contour in enumerate(contours):
    coords = measure.approximate_polygon(contour, tolerance=3)[:-1]
    segmentation = np.flip(coords, axis=1).tolist()
    annotation["shapes"][0]["points"] = segmentation

file = file_name.replace(".jpg", ".json")
with open(file, 'w') as outfile:
    json.dump(annotation, outfile, indent=2)
