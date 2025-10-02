from pydantic_settings import BaseSettings
from typing import Dict, List


class Settings(BaseSettings):
    # Zillow credentials
    zillow_email: str = "YbTenants@gmail.com"
    zillow_password: str = "YbPassw0rd"
    
    # Browser settings
    headless: bool = False
    browser_timeout: int = 30000
    stealth_mode: bool = True
    human_delays: bool = True
    
    # Message processing settings
    check_interval: int = 300  # seconds
    max_retries: int = 3
    
    # Response templates
    response_templates: Dict[str, str] = {
        "tour_requested": (
            "Hi there, to schedule a tour for the apartment you are interested in, "
            "you will need to submit an application through our website yellowbrick.org, "
            "then you will need to send us an email at info@yellowbrick.org to let our "
            "team know you have completed your application. Once your application is "
            "prequalified an appointment can be scheduled to view the apartment. "
            "Thank you!"
        ),
        "application_requested": (
            "Hi there, applications are completed on our website yellowbrick.org. "
            "Once you have submitted your application, contact us at our email us at "
            "info@yellowbrick.org, If you are found eligible we can schedule a showing "
            "for the apartment you are interested in. Thank you!"
        ),
        "homebase_section8_inquiry": (
            "Hi {prospect_name}, yes, we accept the majority of housing assistance "
            "vouchers -Homebase, Section 8, MRVP, Hud Vash, RAFT, etc. Certain "
            "requirements apply. A soft background check is due once the application "
            "is submitted."
        ),
        "homebase_raft_specific": (
            "Although we accept home base and Raft assistance, we require for the "
            "combined household income to meet the requirements of 3 times the rent."
        ),
        "pet_policy": (
            'Please keep in mind we have a strict pet policy. We are happy to make a '
            '"reasonable accommodation" to our pet policy for a registered service '
            'animal, proper documentation required (including registration, '
            'vaccinations etc.).'
        ),
        "general_response_1": (
            "Hi {prospect_name}, yes, the apartment you are inquiring about is still "
            "available. If you are still interested, please submit your application on "
            "our official website yellowbrick.org. Once we can determine you are "
            "eligible for the apartment we can schedule a showing so you can see the "
            "apartment. Please note that we do not schedule showing without a "
            "preapproval of an application, so please email us at info@yellowbrick.org "
            "once you have completed the application. Also, please keep in mind we do "
            "not follow up through Zillow, you will need to reach us directly via "
            "email. Thank you, Yellowbrick Team"
        ),
        "general_response_2": (
            "Hi {prospect_name},\n\n"
            "Thanks so much for your interest — we're excited to let you know that "
            "the apartment you asked about is still available!\n\n"
            "If you'd like to move forward, the next step is to complete an "
            "application on our website at yellowbrick.org. Once we've had a chance "
            "to review and pre-approve your application, we'll be happy to schedule a "
            "showing so you can come see the space in person.\n\n"
            "Just a quick note: we do require pre-approval before scheduling showings. "
            "Once you've submitted your application, please email us at "
            "info@yellowbrick.org to let us know — that way, we can get the process "
            "moving quickly.\n\n"
            "Also, please keep in mind that we don't coordinate through Zillow, so be "
            "sure to contact us directly via email for any updates.\n\n"
            "Looking forward to hearing from you!\n"
            "Warmly,\n\n"
            "The Yellowbrick Team"
        )
    }
    
    # Message classification keywords
    message_keywords: Dict[str, List[str]] = {
        "tour_requested": ["tour", "schedule", "viewing", "showing", "visit"],
        "application_requested": ["application", "apply", "interested", "apply for"],
        "homebase_section8": [
            "homebase", "section 8", "housing assistance", "voucher", 
            "raft", "mrvp", "hud vash", "homebase voucher"
        ],
        "pet_policy": ["pet", "dog", "cat", "animal", "service animal"],
        "general_inquiry": [
            "available", "apartment", "rent", "price", "when", "how much"
        ]
    }
    
    class Config:
        env_file = ".env"

settings = Settings()
