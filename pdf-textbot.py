import os
import logging
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(
    filename="pdf_to_txt.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                text += page.extract_text() + "\n"
                logging.info(f"Extracted text from page {page_num} of {pdf_path}")
            except Exception as e:
                logging.error(f"Error extracting text from page {page_num} of {pdf_path}: {e}")
                raise
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from {pdf_path}: {e}")
        raise

def main():
    try:
        logging.info("Script started.")

        # Get all PDF files in the current directory
        pdf_files = [f for f in os.listdir() if f.endswith(".pdf")]
        if not pdf_files:
            logging.warning("No PDF files found in the current directory.")
            return

        logging.info(f"Found {len(pdf_files)} PDF files.")

        # Prepare the output text file
        output_file = "combined_text.txt"
        with open(output_file, "w", encoding="utf-8") as txt_file:
            for pdf_file in pdf_files:
                logging.info(f"Processing file: {pdf_file}")
                try:
                    # Extract text from each PDF
                    pdf_text = extract_text_from_pdf(pdf_file)
                    txt_file.write(f"--- START OF {pdf_file} ---\n")
                    txt_file.write(pdf_text)
                    txt_file.write(f"--- END OF {pdf_file} ---\n\n")
                    logging.info(f"Successfully processed {pdf_file}.")
                except Exception as e:
                    logging.critical(f"Stopping script due to error with {pdf_file}: {e}")
                    raise

        logging.info(f"Text successfully written to {output_file}.")
    except Exception as e:
        logging.critical(f"Script terminated due to an error: {e}")
    finally:
        logging.info("Script ended.")

if __name__ == "__main__":
    main()
