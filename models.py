from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    TOUR_REQUESTED = "tour_requested"
    APPLICATION_REQUESTED = "application_requested"
    HOMEBASE_SECTION8 = "homebase_section8"
    PET_POLICY = "pet_policy"
    GENERAL_INQUIRY = "general_inquiry"

class MessageStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    REPLIED = "replied"
    ERROR = "error"


class ZillowMessage(BaseModel):
    id: str
    prospect_name: str
    message_content: str
    message_type: Optional[MessageType] = None
    status: MessageStatus = MessageStatus.UNREAD
    timestamp: datetime
    conversation_url: str
    property_address: Optional[str] = None


class MessageResponse(BaseModel):
    success: bool
    message: str
    processed_count: int = 0
    errors: List[str] = []


class ProcessedMessage(BaseModel):
    message_id: str
    prospect_name: str
    message_type: MessageType
    response_sent: bool
    timestamp: datetime
    error_message: Optional[str] = None
