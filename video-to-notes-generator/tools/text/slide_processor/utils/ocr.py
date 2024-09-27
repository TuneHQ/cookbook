# ocr.py

#     Input: Path to an image or image data.
#     Output: Extracted text from the image.
#     Use Cases:
#         Text Recognition:
#             Test: Correctly extract text from a simple image with printed text.
#         Complex Layouts:
#             Test: Extract text from an image with multiple columns or non-standard layouts.
#         Empty Image:
#             Test: Return empty string or placeholder if no text is found.

import os

import pytesseract
from PIL import Image


class OCRProcessor:
    def __init__(self, folder_path, tesseract_cmd=None) -> None:
        self.folder_path = folder_path
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_images(self) -> dict:
        # Get all image files sorted by name
        image_files = sorted(
            [
                f
                for f in os.listdir(self.folder_path)
                if f.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"),
                )
            ],
        )

        extracted_texts = {}

        # Process each image
        for idx, image_file in enumerate(image_files):
            image_path = os.path.join(self.folder_path, image_file)
            text = self.extract_text_from_image(image_path)
            slide_name = f"{idx + 1}"
            extracted_texts[slide_name] = text
            print(f"Processed {slide_name}: {image_file}")

        return extracted_texts

    def extract_text_from_image(self, image_path) -> str:
        # Open the image using PIL
        image = Image.open(image_path)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)

        # Handle empty image cases
        if not text.strip():
            return ""

        return text


# Usage
if __name__ == "__main__":
    folder_path = "tools/text/slide_processor/utils/ocr_samples"

    # tesseract_cmd = r"path_to_your_tesseract_executable"  # Optional: set if not in PATH
    ocr_processor = OCRProcessor(folder_path)
    results = ocr_processor.process_images()

    # Optionally, print the results
    for slide, text in results.items():
        print(f"{slide}:\n{text}\n{'-'*40}")
