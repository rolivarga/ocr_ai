import pytesseract
import cv2
import image_preprocessing
import functions
import os

folder_dir = "test_images/test"
text = ''

for image in os.listdir(folder_dir):
    # Read in the image
    img = cv2.imread(folder_dir + '/' + image)
    
    # Preprocess the image
    img = image_preprocessing.image_preprocessing(img)
    cv2.imwrite("temp/result.jpg", img)
    
    # Detect language
    ocr_result = pytesseract.image_to_string(img)
    lang, prob = functions.detect_language(ocr_result)
    
    # Image to text
    lang_prefix = functions.convert_lang_prefix(lang)
    ocr_result = pytesseract.image_to_string(img, lang=lang_prefix)
    temp_text = functions.remove_empty_lines(ocr_result)
    text = text + temp_text

# Result
result = functions.text_summarize(text, lang)
print(result)