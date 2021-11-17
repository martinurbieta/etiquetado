# %%
import json
import cv2
from shapely.geometry import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
import os
import sys


# * Se abre el label y se queda con el json. Despues de eso el archivo es innecesario por el momento.
def resize_image(filename):
    img = cv2.imread(filename, 1)
    img_half = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    cv2.imwrite(filename, img_half)


def get_label(path_json):
    with open(path_json) as label_file:
        label_json = json.load(label_file)
        label_file.close()
    return label_json


def plot_shape(x_min, y_min, x_max, y_max):
    vertice_1 = (x_min, y_min)
    vertice_2 = (x_min, y_max)
    vertice_3 = (x_max, y_min)
    vertice_4 = (x_max, y_max)
    figura = Polygon([vertice_1, vertice_3, vertice_4, vertice_2])
    # plt.plot(*figura.exterior.xy)
    escalada = figura
    #escalada = affinity.scale(escalada, xfact=scale, yfact=scale)
    plt.plot(*escalada.exterior.xy)


def scale(label_json, scale, jsonfile):
    imageHeight = label_json.get('imageHeight') * scale
    imageWidth = label_json.get('imageWidth') * scale
    label_json['imageHeight'] = imageHeight
    label_json['imageWidth'] = imageWidth
    for shape in label_json.get('shapes'):
        shape_points = shape.get('points')
        for tuple in shape_points:
            for i in range(len(tuple)):
                tuple[i] = tuple[i] * scale

        x_min = min(shape_points[0][0], shape_points[1][0])
        x_max = max(shape_points[0][0], shape_points[1][0])
        y_min = min(shape_points[0][1], shape_points[1][1])
        y_max = max(shape_points[0][1], shape_points[1][1])
        plot_shape(x_min, y_min, x_max, y_max)
    with open(jsonfile, 'w') as f:
        f.write(json.dumps(label_json))
        f.close()


def scale_label(file):
    label = get_label(file)
    scale(label, 0.5, file)


if len(sys.argv) < 1:
    print("Faltan parametros (ruta de carpeta)")
    exit(0)

for filename in os.listdir(sys.argv[1]):
    if filename.endswith(".json"):
        scale_label(filename)
    if filename.endswith(".jpg"):
        resize_image(filename)

# %%
