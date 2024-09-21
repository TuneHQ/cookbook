from tools.text.slide_processor.utils.ocr import OCRProcessor


class ImageHandler:
    def __init__(self, folder_path, tesseract_cmd=None) -> None:
        self.folder_path = folder_path
        self.ocr_processor = OCRProcessor(folder_path, tesseract_cmd)

    def process_images(self) -> dict:
        return self.ocr_processor.process_images()
