import re
from utils.logger import logger

def preprocess_text(text: str) -> str:
    """Standardizes text by removing non-alphanumeric chars and simplifying whitespace."""
    if not text:
        return ""
        
    # Lowercase
    text = text.lower()

    # Remove newlines
    text = re.sub(r'\n', ' ', text)

    # Remove special characters except common punctuation for context
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\(\)]', '', text)

    # Simplify multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()