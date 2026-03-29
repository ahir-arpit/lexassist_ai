import io
from PyPDF2 import PdfReader
from utils.logger import logger

def extract_text(file_bytes: bytes, filename: str = "") -> str:
    """Extracts text from PDF or Plain Text bytes."""
    text = ""
    
    # Check if it's a PDF (PDF magic number %PDF)
    if file_bytes.startswith(b'%PDF'):
        logger.info(f"Extracting text from PDF: {filename}")
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            logger.error(f"PDF Extraction failed: {str(e)}")
            raise ValueError("Invalid PDF format or corrupted file.")
    else:
        # Treat as plain text
        logger.info(f"Extracting text from Plain Text/UTF-8: {filename}")
        try:
            text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1
            text = file_bytes.decode('latin-1')
            
    if not text.strip():
        logger.warning(f"No text extracted from file: {filename}")
        
    return text