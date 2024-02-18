import pytesseract
import cv2
import image_preprocessing
import functions

# Read in the image
image_file = "test_images/eng_book.jpg"
img = cv2.imread(image_file)

# Preprocess the image
img = image_preprocessing.image_preprocessing(img)
cv2.imwrite("temp/result.jpg", img)

# Detect language
ocr_result = pytesseract.image_to_string(img)
lang, prob = functions.detect_language(ocr_result)

# Image to text
lang_prefix = functions.convert_lang_prefix(lang)
ocr_result = pytesseract.image_to_string(img, lang=lang_prefix)
text = functions.remove_empty_lines(ocr_result)

# Result
result = functions.text_summarize(text, lang)
print(result)