import cv2
import ast


def graph_points(x1,x2,y1,y2):
    image = cv2.imread('test_image2.jpg')
    image = cv2.circle(image, (x1, y1), radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, (x2, y1), radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, (x2, y2), radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, (x1, y2), radius=1, color=(0, 0, 255), thickness=-1)
    cv2.imwrite('test_image2.jpg', image)

def graph(t1,t2,t3,t4):
    image = cv2.imread('test_image2.jpg')

    image = cv2.circle(image, t1, radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, t2, radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, t3, radius=1, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, t4, radius=1, color=(0, 0, 255), thickness=-1)

    cv2.imwrite('test_image2.jpg', image)



with open("test_ocr.txt") as ocr_file:
    for x in ocr_file:
        dictionary = ast.literal_eval(x)
        elem = dictionary['points']
        graph(elem[0], elem[1], elem[2], elem[3])


"""with open("test_prediction.txt") as pred_file:
    for x in pred_file:
        dictionary = ast.literal_eval(x)
        elem = dictionary["points"]
        graph_points(int(elem["x1"]), int(elem["x2"]), int(elem["y1"]) - 160, int(elem["y2"])-160)
"""