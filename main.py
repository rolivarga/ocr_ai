import pytesseract
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np
import image_preprocessing
import helper_functions

# Read in the image
image_file = "test_images/eng_book.jpg"
img = cv2.imread(image_file)

# Preprocess the image
image_preprocessing.image_preprocessing(img)
cv2.imwrite("temp/result.jpg", img)

# Image to text
ocr_result = pytesseract.image_to_string(img)

text = helper_functions.remove_empty_lines(ocr_result)
print(text)