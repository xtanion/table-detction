import cv2
from PIL import Image
import pytesseract
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import math
from key_items import filter_text

# filename = 'filters/data/min.jpg'


def ocr_image(filename):
    img = np.array(Image.open(filename))

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, None, fx=2, fy=2)
    shape = img.shape
    plt.imshow(img, cmap='gray')
    plt.show()

    img_edges = cv2.Canny(img_grey, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, np.pi / 180.0,
                            100, minLineLength=100, maxLineGap=5)

    angles = []

    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_grey, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # cv2.imshow("Detected lines", img_grey)
    # key = cv2.waitKey(0)

    median_angle = np.median(angles)
    diff_angle = min(min(angles), 180)
    img_rotated = ndimage.rotate(img, median_angle)
    # img_rotated = img_rotated[0:shape[1], 0:shape[0]]

    plt.imshow(img_rotated, cmap='gray')
    plt.show()

    # text extraction
    text = pytesseract.image_to_string(img_rotated, lang='eng')

    # file1 = open("myfile.txt", "w")  # write mode
    # file1.write(text)
    # file1.close()

    out = filter_text(text)
    return out


ocr_image('filters/data/min.jpg')