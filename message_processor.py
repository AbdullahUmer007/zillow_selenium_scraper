import asyncio
from typing import List, Optional
from loguru import logger
from models import ZillowMessage, ProcessedMessage, MessageResponse, MessageStatus
from message_classifier import MessageClassifier
from zillow_selenium_scraper import ZillowSeleniumScraper
from config import settings

class MessageProcessor:
    """Handles message processing and automated replies"""
    
    def __init__(self):
        self.classifier = MessageClassifier()
        self.scraper = ZillowSeleniumScraper()
        self.processed_messages = []
    
    def process_unread_messages(self, email: str, password: str) -> MessageResponse:
        """Process all unread messages and send appropriate replies"""
        try:
            # Initialize scraper and login
            self.scraper.initialize()
            login_success = self.scraper.login(email, password)
            
            if not login_success:
                return MessageResponse(
                    success=False,
                    message="Failed to login to Zillow",
                    errors=["Login failed"]
                )
            
            # Get unread messages
            unread_messages = self.scraper.get_unread_messages()
            
            if not unread_messages:
                return MessageResponse(
                    success=True,
                    message="No unread messages found",
                    processed_count=0
                )
            
            logger.info(f"Found {len(unread_messages)} unread messages to process")
            
            processed_count = 0
            errors = []
            
            for message in unread_messages:
                try:
                    result = self._process_single_message(message)
                    if result:
                        processed_count += 1
                        self.processed_messages.append(result)
                except Exception as e:
                    error_msg = f"Failed to process message {message.id}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            self.scraper.close()
            
            return MessageResponse(
                success=True,
                message=f"Processed {processed_count} messages successfully",
                processed_count=processed_count,
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Error in process_unread_messages: {e}")
            self.scraper.close()
            return MessageResponse(
                success=False,
                message=f"Error processing messages: {str(e)}",
                errors=[str(e)]
            )
    
    def _process_single_message(self, message: ZillowMessage) -> Optional[ProcessedMessage]:
        """Process a single message and send appropriate reply"""
        try:
            # Classify the message
            message_type = self.classifier.classify_message(
                message.message_content, 
                message.prospect_name
            )
            
            logger.info(f"Processing message from {message.prospect_name} - Type: {message_type}")
            
            # Get response template
            response_template = self.classifier.get_response_template(
                message_type, 
                message.prospect_name
            )
            
            # Add additional information if needed
            full_response = self._build_complete_response(
                response_template, 
                message_type, 
                message.message_content,
                message.prospect_name
            )
            
            # Open conversation and send reply
            conversation_opened = self.scraper.open_conversation(message.conversation_url)
            
            if not conversation_opened:
                logger.error(f"Failed to open conversation for message {message.id}")
                return ProcessedMessage(
                    message_id=message.id,
                    prospect_name=message.prospect_name,
                    message_type=message_type,
                    response_sent=False,
                    timestamp=message.timestamp,
                    error_message="Failed to open conversation"
                )
            
            # Send the reply
            reply_sent = self.scraper.send_reply(full_response)
            
            if reply_sent:
                logger.info(f"Successfully sent reply to {message.prospect_name}")
                return ProcessedMessage(
                    message_id=message.id,
                    prospect_name=message.prospect_name,
                    message_type=message_type,
                    response_sent=True,
                    timestamp=message.timestamp
                )
            else:
                logger.error(f"Failed to send reply to {message.prospect_name}")
                return ProcessedMessage(
                    message_id=message.id,
                    prospect_name=message.prospect_name,
                    message_type=message_type,
                    response_sent=False,
                    timestamp=message.timestamp,
                    error_message="Failed to send reply"
                )
                
        except Exception as e:
            logger.error(f"Error processing message {message.id}: {e}")
            return ProcessedMessage(
                message_id=message.id,
                prospect_name=message.prospect_name,
                message_type=message_type if 'message_type' in locals() else None,
                response_sent=False,
                timestamp=message.timestamp,
                error_message=str(e)
            )
    
    def _build_complete_response(self, base_response: str, message_type, content: str, prospect_name: str) -> str:
        """Build a complete response with additional information if needed"""
        response_parts = [base_response]
        
        # Add pet policy information for tour and application requests
        if self.classifier.should_include_pet_policy(message_type, content):
            pet_policy = settings.response_templates["pet_policy"]
            response_parts.append(f"\n\n{pet_policy}")
        
        # Add homebase/raft specific information
        if self.classifier.should_include_homebase_raft(message_type, content):
            homebase_raft = settings.response_templates["homebase_raft_specific"]
            response_parts.append(f"\n\n{homebase_raft}")
        
        return "\n".join(response_parts)
    
    def get_processed_messages(self) -> List[ProcessedMessage]:
        """Get list of processed messages"""
        return self.processed_messages
    
    def clear_processed_messages(self):
        """Clear the list of processed messages"""
        self.processed_messages = []
