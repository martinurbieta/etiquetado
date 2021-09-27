import cv2

image = cv2.imread('test_image2.jpg')

x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))
x2 = int(input("Enter x1: "))
y2 = int(input("Enter y1: "))
image = cv2.circle(image, (x1, y1), radius=1, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (x2, y1), radius=1, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (x2, y2), radius=1, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (x1, y2), radius=1, color=(0, 0, 255), thickness=-1)

cv2.imwrite('test_image2.jpg', image)

