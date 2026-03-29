from fastapi import APIRouter, UploadFile, File
from services.pdf_extractor import extract_text
from services.text_preprocessor import preprocess_text
from services.ner_module import extract_entities
from services.risk_analyzer import analyze_risk
from services.summarizer import generate_summary
from services.statutory_comparer import compare_with_law
from models.schemas import AnalysisResponse
from utils.logger import logger

router = APIRouter(tags=["Analysis"])

@router.post("/upload-contract", response_model=AnalysisResponse)
async def upload_contract(file: UploadFile = File(...)):
    filename = file.filename
    logger.info(f"Received contract for analysis: {filename}")
    
    try:
        contents = await file.read()
        
        # 1. Extraction
        text = extract_text(contents, filename)
        
        # 2. Preprocessing
        logger.info(f"Preprocessing text for {filename}...")
        clean_text = preprocess_text(text)
        
        # 3. Logic Execution
        logger.info(f"Running NER, Risk, and Summary modules for {filename}...")
        entities = extract_entities(clean_text)
        risk = analyze_risk(clean_text)
        summary = generate_summary(clean_text)
        statutory = compare_with_law(clean_text)
        
        logger.info(f"Analysis complete for {filename}. Status: Success")
        
        return {
            "filename": filename,
            "entities": entities,
            "risk_analysis": risk,
            "summary": summary,
            "statutory_comparison": statutory,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Analysis failed for {filename}: {str(e)}", exc_info=True)
        raise e