from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.upload_routes import router as upload_router
from utils.logger import logger
import time

app = FastAPI(
    title="LexAssist AI Backend",
    description="Professional Legal Document Analysis API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal Server Error. Please contact support."}
    )

# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Completed in {process_time:.4f}s")
    return response

app.include_router(upload_router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time(), "version": "1.0.0"}

@app.get("/")
def home():
    return {
        "message": "LexAssist AI Backend - Modern Legal Analysis Engine",
        "docs": "/docs",
        "health": "/health"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("LexAssist AI Backend Starting up...")
    logger.info("Initializing Legal Models...")