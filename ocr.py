import easyocr
import os

# Initialize OCR reader (English)
reader = easyocr.Reader(['en'])

def image_to_text(image_path):
    """
    Extract text from an image using EasyOCR.
    """
    if not os.path.exists(image_path):
        return "Image file not found."

    try:
        result = reader.readtext(image_path, detail=0)
        text = " ".join(result)

        if text.strip() == "":
            return "No text found in the image."

        return text

    except Exception as e:
        return f"OCR Error: {str(e)}"