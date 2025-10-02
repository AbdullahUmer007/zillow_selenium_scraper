import time
import random
import asyncio
from datetime import datetime
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from selenium_stealth import stealth
from loguru import logger
from models import ZillowMessage, MessageStatus
from config import settings

class ZillowSeleniumScraper:
    """Selenium-based Zillow message scraper with advanced anti-detection"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.is_logged_in = False
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
    
    def initialize(self):
        """Initialize undetected Chrome driver with stealth settings"""
        try:
            # Use undetected-chromedriver for better evasion
            options = uc.ChromeOptions()
            
            # Basic options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=TranslateUI')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-prompt-on-repost')
            options.add_argument('--disable-hang-monitor')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-translate')
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-extensions-with-background-pages')
            options.add_argument('--disable-domain-reliability')
            options.add_argument('--disable-features=AudioServiceOutOfProcess')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--safebrowsing-disable-auto-update')
            options.add_argument('--password-store=basic')
            options.add_argument('--use-mock-keychain')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-windows10-custom-titlebar')
            
            # Anti-detection options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-plugins-discovery')
            options.add_argument('--disable-preconnect')
            options.add_argument('--disable-print-preview')
            options.add_argument('--disable-save-password-bubble')
            options.add_argument('--disable-single-click-autofill')
            options.add_argument('--disable-speech-api')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-xss-auditor')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-extensions-with-background-pages')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-features=TranslateUI')
            options.add_argument('--disable-hang-monitor')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-prompt-on-repost')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-translate')
            options.add_argument('--disable-windows10-custom-titlebar')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--no-first-run')
            options.add_argument('--safebrowsing-disable-auto-update')
            options.add_argument('--password-store=basic')
            options.add_argument('--use-mock-keychain')
            
            # User agent
            options.add_argument(f'--user-agent={random.choice(self.user_agents)}')
            
            # Window size
            options.add_argument('--window-size=1920,1080')
            
            # Headless mode
            if settings.headless:
                options.add_argument('--headless=new')
            
            # Initialize undetected Chrome driver

            # self.driver = uc.Chrome(options=options, version_main=None)
            self.driver = uc.Chrome()
            # Apply stealth settings
            stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            
            # Execute additional stealth scripts
            # self.driver.execute_script("""
            #     Object.defineProperty(navigator, 'webdriver', {
            #         get: () => undefined,
            #     });
            #
            #     Object.defineProperty(navigator, 'plugins', {
            #         get: () => [1, 2, 3, 4, 5],
            #     });
            #
            #     Object.defineProperty(navigator, 'languages', {
            #         get: () => ['en-US', 'en'],
            #     });
            #
            #     Object.defineProperty(navigator, 'hardwareConcurrency', {
            #         get: () => 4,
            #     });
            #
            #     Object.defineProperty(navigator, 'deviceMemory', {
            #         get: () => 8,
            #     });
            #
            #     Object.defineProperty(navigator, 'maxTouchPoints', {
            #         get: () => 0,
            #     });
            #
            #     window.chrome = {
            #         runtime: {},
            #     };
            #
            #     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            #     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            #     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            # """)
            #
            logger.info("Selenium driver initialized successfully with anti-detection measures")
            
        except Exception as e:
            logger.error(f"Failed to initialize Selenium driver: {e}")
            raise
    
    def human_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add human-like random delays"""
        if not settings.human_delays:
            return
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_type(self, element, text: str):
        """Type text with human-like delays between keystrokes"""
        element.click()
        self.human_delay(0.1, 0.3)
        
        for char in text:
            element.send_keys(char)
            if settings.human_delays:
                time.sleep(random.uniform(0.05, 0.15))
    
    def human_click(self, element):
        """Click element with human-like behavior"""
        # Move mouse to element first
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.human_delay(0.1, 0.3)
        
        # Click with slight randomness
        actions.click(element).perform()
        self.human_delay(0.5, 1.5)
    
    def login(self, email: str, password: str) -> bool:
        """Login to Zillow with human-like behavior"""
        try:
            if not self.driver:
                self.initialize()
            
            logger.info("Navigating to Zillow login page")
            self.driver.get("https://www.zillow.com/user/acct/login?url=%2Frental-manager%2Finbox%3Fap%3Dx")
            self.human_delay(2, 4)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for page to fully load
            self.human_delay(1, 2)
            
            # Fill login form with human-like behavior
            try:
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "reg-login-email"))
                )
                self.human_type(email_input, email)
                self.human_delay(1, 2)
                
                password_input = self.driver.find_element(By.ID, "inputs-password")
                self.human_type(password_input, password)
                self.human_delay(1, 3)
                
                # Click login button with human-like behavior
                login_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
                self.human_click(login_button)
                
                # Wait for login to process
                self.human_delay(3, 5)
                
                # Check if login was successful
                try:
                    # Look for various success indicators
                    success_selectors = [
                        '.swipeable-list-item__content',
                        '.rental-manager',
                        '.inbox',
                        '[data-testid="header"]',
                        '.user-menu',
                        '.profile-menu',
                        '[data-testid="conversation-item"]'
                    ]
                    
                    success = False
                    time.sleep(5)
                    if 'rental-manager/inbox' in self.driver.current_url:
                        success = True
                    
                    if success:
                        self.is_logged_in = True
                        logger.info("Successfully logged in to Zillow")
                        return True
                    return False
                        
                except Exception as e:
                    logger.error(f"Login verification failed: {e}")
                    return False
                    
            except TimeoutException:
                logger.error("Login form elements not found")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def navigate_to_messages(self) -> bool:
        """Navigate to the messages section with human-like behavior"""
        try:
            if not self.is_logged_in:
                logger.error("Must be logged in to access messages")
                return False
            
            logger.info("Navigating to messages section")
            self.driver.get("https://www.zillow.com/rental-manager/inbox/")
            self.human_delay(2, 4)
            
            # Wait for messages to load with multiple possible selectors
            message_selectors = [
                '[data-testid="message-list"]',
                '.message-list',
                '.messages-container',
                '.conversation-list',
                '[class*="message"]',
                '.inbox'
            ]
            
            messages_loaded = False
            for selector in message_selectors:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    messages_loaded = True
                    break
                except TimeoutException:
                    continue
            
            if messages_loaded:
                logger.info("Successfully navigated to messages")
                return True
            else:
                logger.warning("Messages section loaded but no message list found")
                return True  # Still return True as page loaded
            
        except Exception as e:
            logger.error(f"Failed to navigate to messages: {e}")
            return False
    
    def get_unread_messages(self) -> List[ZillowMessage]:
        """Get all unread messages from the messages panel"""
        try:
            messages = []
            
            # Look for conversation items with unread badges
            conversation_items = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="conversation-item"]')
            
            unread_elements = []
            for item in conversation_items:
                try:
                    # Check if this conversation has an unread badge
                    unread_badge = item.find_elements(By.CSS_SELECTOR, '[data-testid="unread-badge"]')
                    if unread_badge:
                        unread_elements.append(item)
                except:
                    continue
            
            logger.info(f"Found {len(unread_elements)} unread messages")
            
            for element in unread_elements:
                try:
                    message_data = self._extract_message_data(element)
                    if message_data:
                        messages.append(message_data)
                except Exception as e:
                    logger.error(f"Failed to extract message data: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get unread messages: {e}")
            return []
    
    def _extract_message_data(self, element) -> Optional[ZillowMessage]:
        """Extract message data from a message element"""
        try:
            # Extract prospect name from data-testid="participant-name"
            prospect_name = "Unknown"
            try:
                name_element = element.find_element(By.CSS_SELECTOR, '[data-testid="participant-name"]')
                prospect_name = name_element.text.strip()
            except NoSuchElementException:
                logger.warning("Could not find participant name")
            
            # Extract message content from the message preview
            message_content = ""
            try:
                # Look for the message preview paragraph (not the "You:" part)
                message_preview = element.find_element(By.CSS_SELECTOR, '[data-testid="message-preview"]')
                # Get the paragraph that contains the actual message content
                message_paragraph = message_preview.find_element(By.CSS_SELECTOR, 'p[data-c11n-component="Paragraph"]')
                message_content = message_paragraph.text.strip()
                
                # Remove "You:" prefix if it exists (for sent messages)
                if message_content.startswith("You:"):
                    message_content = message_content[4:].strip()
                    
            except NoSuchElementException:
                logger.warning("Could not find message content")
            
            # Extract property address from data-testid="address"
            property_address = None
            try:
                address_element = element.find_element(By.CSS_SELECTOR, '[data-testid="address"]')
                property_address = address_element.text.strip()
            except NoSuchElementException:
                logger.warning("Could not find property address")
            
            # Extract conversation ID from the li element's id attribute
            conversation_id = element.get_attribute('id')
            
            # Build conversation URL (Zillow's pattern)
            conversation_url = f"https://www.zillow.com/rental-manager/inbox/{conversation_id}/"
            
            # Extract message type from status label
            message_type = None
            try:
                status_element = element.find_element(By.CSS_SELECTOR, '[data-testid="status-label"] span')
                status_text = status_element.text.strip()
                # Map Zillow status to our message types
                if "APPLICATION REQUESTED" in status_text:
                    message_type = "application_requested"
                elif "TOUR REQUESTED" in status_text:
                    message_type = "tour_requested"
                elif "INQUIRY" in status_text:
                    message_type = "general_inquiry"
            except NoSuchElementException:
                logger.warning("Could not find status label")
            
            # Generate a unique ID
            message_id = f"zillow_{conversation_id}_{hash(prospect_name + message_content)}"
            
            logger.info(f"Extracted message: {prospect_name} - {message_content[:50]}...")
            
            return ZillowMessage(
                id=message_id,
                prospect_name=prospect_name,
                message_content=message_content,
                status=MessageStatus.UNREAD,
                timestamp=datetime.now(),
                conversation_url=conversation_url,
                property_address=property_address
            )
            
        except Exception as e:
            logger.error(f"Failed to extract message data: {e}")
            return None
    
    def open_conversation(self, conversation_url: str) -> bool:
        """Open a specific conversation by clicking on it"""
        try:
            if not conversation_url:
                return False
            
            # Extract conversation ID from URL
            conversation_id = conversation_url.split('/')[-2] if conversation_url.endswith('/') else conversation_url.split('/')[-1]
            
            # Find the conversation item by its ID
            conversation_element = self.driver.find_element(By.CSS_SELECTOR, f'[data-testid="conversation-item"][id="{conversation_id}"]')
            
            # Click on the conversation to open it
            self.human_click(conversation_element)
            self.human_delay(2, 4)
            
            # Wait for conversation to load
            try:
                # Look for conversation view elements
                conversation_selectors = [
                    '[data-testid="message-item"]'
                ]
                
                conversation_loaded = False
                for selector in conversation_selectors:
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        conversation_loaded = True
                        break
                    except TimeoutException:
                        continue
                
                if conversation_loaded:
                    logger.info(f"Opened conversation: {conversation_id}")
                    return True
                else:
                    logger.error(f"Conversation did not load: {conversation_id}")
                    return False
                    
            except TimeoutException:
                logger.error(f"Conversation did not load: {conversation_id}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to open conversation {conversation_url}: {e}")
            return False
    
    def send_reply(self, message: str) -> bool:
        """Send a reply in the current conversation with human-like behavior"""
        try:
            # First, try to find and click on the "Choose saved reply" button to reveal message input
            # Look for message input field
            message_input = None
            try:
                self.driver.find_element(By.XPATH,
                                         "//li[@data-testid='message-item' and contains(@aria-label, 'You sent')][last()]//div[@data-testid='chat-bubble']/p").text
                return False
            except:
                pass
            # Try to find textarea with specific placeholder text
            textarea_selectors = [
                '[aria-label="Message input;"]'
            ]
            
            for selector in textarea_selectors:
                try:
                    message_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # Check if it's visible and enabled
                    if message_input.is_displayed() and message_input.is_enabled():
                        break
                    else:
                        message_input = None
                except NoSuchElementException:
                    continue
            
            # Clear any existing text and type the message with human-like behavior
            message_input.clear()
            self.human_delay(0.5, 1.0)
            self.human_type(message_input, message)
            self.human_delay(1, 2)

            # Find and click send button - look for Enter key or send button
            # First try to find a send button
            send_selectors = [
                'button.send-message-button'
            ]

            send_button = None
            for selector in send_selectors:
                try:
                    send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue

            if send_button:
                # Click send with human-like behavior
                self.human_click(send_button)
                self.human_delay(2, 4)
                return True
            return True
        except Exception as e:
            logger.error(f"Failed to send reply: {e}")
            return False
    
    def close(self):
        """Close browser and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
