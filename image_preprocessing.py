import cv2
import numpy as np

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return crop

def image_preprocessing(img):
    # gray
    gray_image = grayscale(img)
    cv2.imwrite("temp/gray.jpg", gray_image)

    # binary image
    thresh, im_bw = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite("temp/bw_image.jpg", im_bw)

    # noise removal
    no_noise = noise_removal(im_bw)
    cv2.imwrite("temp/no_noise.jpg", no_noise)

    # thin font
    eroded_image = thin_font(no_noise)
    cv2.imwrite("temp/eroded_image.jpg", eroded_image)

    # no borders
    no_borders = remove_borders(no_noise)
    cv2.imwrite("temp/no_borders.jpg", no_borders)

    return no_borders