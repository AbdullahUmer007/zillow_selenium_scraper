from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from loguru import logger
import sys

from models import MessageResponse, ProcessedMessage, ZillowMessage
from message_processor import MessageProcessor
from config import settings

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

app = FastAPI(
    title="Zillow Message Auto-Reply API",
    description="Automated message processing and reply system for Zillow messages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global message processor instance
message_processor = MessageProcessor()

class LoginRequest(BaseModel):
    email: str
    password: str

class ProcessMessagesRequest(BaseModel):
    auto_process: bool = True

class ProcessedMessagesResponse(BaseModel):
    processed_messages: List[ProcessedMessage]
    total_count: int

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Zillow Message Auto-Reply API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/login", response_model=dict)
async def login():
    """Test login credentials from .env file"""
    try:
        if not settings.zillow_email or not settings.zillow_password:
            raise HTTPException(
                status_code=400, 
                detail="Zillow credentials not configured in .env file"
            )
        
        processor = MessageProcessor()
        processor.scraper.initialize()
        login_success = processor.scraper.login(
            settings.zillow_email, 
            settings.zillow_password
        )
        processor.scraper.close()
        
        if login_success:
            return {"success": True, "message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Login failed")
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/process-messages", response_model=MessageResponse)
async def process_messages(request: ProcessMessagesRequest):
    """Process unread messages and send automated replies"""
    try:
        if not settings.zillow_email or not settings.zillow_password:
            raise HTTPException(
                status_code=400, 
                detail="Zillow credentials not configured in .env file"
            )
        
        logger.info(f"Starting message processing for {settings.zillow_email}")
        
        result = message_processor.process_unread_messages(
            settings.zillow_email, 
            settings.zillow_password
        )
        
        logger.info(f"Message processing completed: {result.message}")
        return result
        
    except Exception as e:
        logger.error(f"Error in process_messages endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing messages: {str(e)}")

@app.get("/processed-messages", response_model=ProcessedMessagesResponse)
async def get_processed_messages():
    """Get list of processed messages"""
    try:
        processed = message_processor.get_processed_messages()
        return ProcessedMessagesResponse(
            processed_messages=processed,
            total_count=len(processed)
        )
    except Exception as e:
        logger.error(f"Error getting processed messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving processed messages: {str(e)}")

@app.delete("/processed-messages")
async def clear_processed_messages():
    """Clear the list of processed messages"""
    try:
        message_processor.clear_processed_messages()
        return {"success": True, "message": "Processed messages cleared"}
    except Exception as e:
        logger.error(f"Error clearing processed messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing processed messages: {str(e)}")

@app.get("/message-templates")
async def get_message_templates():
    """Get available message response templates"""
    try:
        return {
            "templates": settings.response_templates,
            "message_types": {
                "tour_requested": "Tour Requested",
                "application_requested": "Application Requested", 
                "homebase_section8_inquiry": "Homebase/Section 8 Inquiry",
                "pet_policy": "Pet Policy",
                "general_response_1": "General Response 1",
                "general_response_2": "General Response 2"
            }
        }
    except Exception as e:
        logger.error(f"Error getting message templates: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")

@app.post("/test-classification")
async def test_message_classification(message_content: str, prospect_name: str = ""):
    """Test message classification without sending replies"""
    try:
        from message_classifier import MessageClassifier
        classifier = MessageClassifier()
        
        message_type = classifier.classify_message(message_content, prospect_name)
        response_template = classifier.get_response_template(message_type, prospect_name)
        
        return {
            "message_content": message_content,
            "prospect_name": prospect_name,
            "classified_type": message_type,
            "response_template": response_template
        }
    except Exception as e:
        logger.error(f"Error in test classification: {e}")
        raise HTTPException(status_code=500, detail=f"Error testing classification: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
