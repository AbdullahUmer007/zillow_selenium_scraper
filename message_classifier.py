from models import MessageType
from config import settings


class MessageClassifier:
    """Classifies Zillow messages based on content and keywords"""
    
    def __init__(self):
        self.keywords = settings.message_keywords
    
    def classify_message(self, message_content: str, 
                        prospect_name: str = "") -> MessageType:
        """
        Classify a message based on its content
        """
        content_lower = message_content.lower()
        
        # Check for specific message types in order of priority
        if self._contains_keywords(content_lower, 
                                  self.keywords["tour_requested"]):
            return MessageType.TOUR_REQUESTED
            
        if self._contains_keywords(content_lower, 
                                  self.keywords["application_requested"]):
            return MessageType.APPLICATION_REQUESTED
            
        if self._contains_keywords(content_lower, 
                                  self.keywords["homebase_section8"]):
            return MessageType.HOMEBASE_SECTION8
            
        if self._contains_keywords(content_lower, 
                                  self.keywords["pet_policy"]):
            return MessageType.PET_POLICY
            
        # Default to general inquiry
        return MessageType.GENERAL_INQUIRY
    
    def _contains_keywords(self, content: str, keywords: list) -> bool:
        """Check if content contains any of the specified keywords"""
        for keyword in keywords:
            if keyword in content:
                return True
        return False
    
    def get_response_template(self, message_type: MessageType, 
                            prospect_name: str = "") -> str:
        """Get the appropriate response template based on message type"""
        template_key = message_type.value
        
        if template_key in settings.response_templates:
            template = settings.response_templates[template_key]
            return template.format(prospect_name=prospect_name or "there")
        
        # Fallback to general response
        return settings.response_templates["general_response_1"].format(
            prospect_name=prospect_name or "there"
        )
    
    def should_include_pet_policy(self, message_type: MessageType, 
                                 content: str) -> bool:
        """Determine if pet policy should be included in response"""
        return message_type in [
            MessageType.TOUR_REQUESTED, 
            MessageType.APPLICATION_REQUESTED
        ]
    
    def should_include_homebase_raft(self, message_type: MessageType, 
                                    content: str) -> bool:
        """Determine if homebase/raft specific info should be included"""
        content_lower = content.lower()
        return (message_type == MessageType.HOMEBASE_SECTION8 and 
                any(keyword in content_lower for keyword in ["homebase", "raft"]))
