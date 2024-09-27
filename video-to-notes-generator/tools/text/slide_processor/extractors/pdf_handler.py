import fitz  # Import the PyMuPDF library


def extract_text_from_pdf(pdf_file_path) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.

    """
    try:
        # Open the PDF file
        doc = fitz.open(pdf_file_path)

        # Initialize an empty string to store the text
        text = ""

        # Iterate through each page in the PDF
        for page in doc:
            # Extract the text from the page and add it to the text string
            text += page.get_text()

        # Close the PDF file
        doc.close()

        # Return the extracted text
        return text

    except fitz.FitzError as e:
        # Handle the error if the PDF file cannot be read
        print(f"Error: Unable to read the PDF file {pdf_file_path}. Details: {e}")
        return None

    except Exception as e:
        # Handle any other errors
        print(f"An error occurred: {e}")
        return None


# Example usage
pdf_file_path = "resume1.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    print("Extracted Text:")
    print("-------------------------------")
    print(extracted_text)
    print("-------------------------------")
else:
    print("No text found in the PDF file.")
