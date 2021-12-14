# %%
import json
import cv2
from shapely.geometry import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
import os
import sys
import base64

# * Se abre el label y se queda con el json. Despues de eso el archivo es innecesario por el momento.


def resize_image(image):
    img_half = cv2.resize(image, (0, 0), fx=0.3, fy=0.3)
    cv2.imwrite(image, img_half)


def get_label(filename):
    with open(f'{filename}.json') as label_file:
        label_json = json.load(label_file)
    return label_json


def crop_area(shape_points, image, idx):
    x_min = min(shape_points[0][0], shape_points[1][0])
    x_max = max(shape_points[0][0], shape_points[1][0])
    y_min = min(shape_points[0][1], shape_points[1][1])
    y_max = max(shape_points[0][1], shape_points[1][1])
    ############## CAMBIAR ACA ####################
    height, width, idk = image.shape
    x_left = int(x_min - 500)
    x_right = int(x_max + 500)
    y_top = int(y_min - 500)
    y_bottom = int(y_max + 500)

    label_w = x_max - x_min
    label_h = y_max - y_min

    vertice1 = [500, 500]
    vertice2 = [500+label_w, 500+label_h]
    points = [vertice1, vertice2]

    crop_w = x_right - x_left
    crop_h = y_bottom - y_top

    if x_left >= 0 and y_top >= 0 and x_right <= width and y_bottom <= height:
        left = x_left
        right = x_left + crop_w
        top = y_top
        bottom = y_top + crop_h
        return left, right, top, bottom, points
    else:
        height, width, idk = image.shape
        x_left = int(x_min - 100)
        x_right = int(x_max + 100)
        y_top = int(y_min - 100)
        y_bottom = int(y_max + 100)

        label_w = x_max - x_min
        label_h = y_max - y_min

        vertice1 = [100, 100]
        vertice2 = [100+label_w, 100+label_h]
        points = [vertice1, vertice2]

        crop_w = x_right - x_left
        crop_h = y_bottom - y_top

        if x_left >= 0 and y_top >= 0 and x_right <= width and y_bottom <= height:
            left = x_left
            right = x_left + crop_w
            top = y_top
            bottom = y_top + crop_h
            return left, right, top, bottom, points


def create_json(label_json, filename, idx, shape, points, image_shape):

    new_json = label_json
    shape['points'] = points
    new_json['shapes'] = [shape]
    new_json['imagePath'] = '{filename}_crop_{idx}.jpg'
    new_json['imageHeight'] = image_shape[1]
    new_json['imageWidth'] = image_shape[0]

    img = cv2.imread(f'Filtradas/{filename}_crop_{idx}.jpg')
    _, encoded_img = cv2.imencode('.png', img)  # Works for '.jpg' as well
    base64_img = base64.b64encode(encoded_img).decode("utf-8")
    new_json['imageData'] = base64_img

    with open(f'Filtradas/{filename}_crop_{idx}.json', 'w') as f:
        f.write(json.dumps(new_json))

    return


def to_image_string(image_filepath):
    return open(image_filepath, 'rb').read().encode('base64')


def crop_shape(shape_points, image, filename, idx, label_json):

    # Obtiene medidas para el corte y los nuevos puntos de la figura
    left, right, top, bottom, points = crop_area(
        shape_points, image, idx)

    dirExist = os.path.exists(filename)
    if not dirExist:
        os.mkdir(filename)

    # Realiza el corte
    cropped = image[top:bottom, left:right]

    x, y, z = cropped.shape

    ###################### CAMBIAR ACA ################################
    if x < 1600 and y < 1600:
        cv2.imwrite(f'Filtradas/{filename}_crop_{idx}.jpg', cropped)

        # Retorna lo neceario para generar el json
        return points, cropped.shape
    return None, None


def split_master_9000(filename):
    image = cv2.imread(f'{filename}.jpg', 1)
    label_json = get_label(filename)

    for idx, shape in enumerate(label_json.get('shapes')):
        if shape['shape_type'] == "rectangle":
            shape_points = shape.get('points')
            points, im_shape = crop_shape(
                shape_points, image, filename, idx, label_json)

            if points and im_shape:
                create_json(label_json, filename, idx, shape, points, im_shape)


if __name__ == '__main__':
    for filename in os.listdir('.'):
        if filename.endswith('.jpg'):
            split_master_9000(filename.split('.')[0])
