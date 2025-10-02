# Zillow Message Auto-Reply API

An automated system that processes Zillow rental inquiries and sends appropriate responses based on message classification.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Zillow credentials in `config.py` or create a `.env` file:
```
ZILLOW_EMAIL=your_email@example.com
ZILLOW_PASSWORD=your_password
```

3. Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health`
- Check if the API is running
- Response: `{"status": "healthy", "message": "API is running"}`

### Test Login
- **POST** `/login`
- Test your Zillow credentials
- Response: `{"success": true, "message": "Login successful"}`

### Process Messages
- **POST** `/process-messages`
- Process all unread Zillow messages and send automated replies
- Body: `{"auto_process": true}`
- Response: 
```json
{
  "success": true,
  "message": "Processed 3 messages successfully",
  "processed_count": 3,
  "errors": []
}
```

### Get Processed Messages
- **GET** `/processed-messages`
- Retrieve list of all processed messages
- Response:
```json
{
  "processed_messages": [
    {
      "message_id": "zillow_123_456",
      "prospect_name": "John Doe",
      "message_type": "tour_requested",
      "response_sent": true,
      "timestamp": "2024-01-15T10:30:00",
      "error_message": null
    }
  ],
  "total_count": 1
}
```

### Clear Processed Messages
- **DELETE** `/processed-messages`
- Clear the list of processed messages
- Response: `{"success": true, "message": "Processed messages cleared"}`

### Get Message Templates
- **GET** `/message-templates`
- View all available response templates
- Response:
```json
{
  "templates": {
    "tour_requested": "Hi there, to schedule a tour...",
    "application_requested": "Hi there, applications are completed...",
    "general_response_1": "Hi {prospect_name}, yes, the apartment..."
  },
  "message_types": {
    "tour_requested": "Tour Requested",
    "application_requested": "Application Requested",
    "homebase_section8_inquiry": "Homebase/Section 8 Inquiry"
  }
}
```

### Test Message Classification
- **POST** `/test-classification`
- Test how a message would be classified without sending a reply
- Body: `"Hi, I'd like to schedule a tour of the apartment"`
- Response:
```json
{
  "message_content": "Hi, I'd like to schedule a tour of the apartment",
  "prospect_name": "",
  "classified_type": "tour_requested",
  "response_template": "Hi there, to schedule a tour for the apartment..."
}
```

## Message Types

The system automatically classifies messages into these categories:

- **Tour Requested** - Messages asking to schedule viewings
- **Application Requested** - Messages about applying for apartments
- **Homebase/Section 8** - Housing assistance inquiries
- **Pet Policy** - Questions about pets and service animals
- **General Inquiry** - General availability and pricing questions

## Usage Examples

### Using curl:

```bash
# Test login
curl -X POST http://localhost:8000/login

# Process messages
curl -X POST http://localhost:8000/process-messages \
  -H "Content-Type: application/json" \
  -d '{"auto_process": true}'

# Get processed messages
curl -X GET http://localhost:8000/processed-messages

# Test classification
curl -X POST http://localhost:8000/test-classification \
  -H "Content-Type: application/json" \
  -d '"I want to apply for this apartment"'
```

### Using Python requests:

```python
import requests

# Process messages
response = requests.post(
    "http://localhost:8000/process-messages",
    json={"auto_process": True}
)
print(response.json())

# Get processed messages
response = requests.get("http://localhost:8000/processed-messages")
print(response.json())
```

## Configuration

Key settings in `config.py`:

- `headless`: Run browser in headless mode (default: False)
- `stealth_mode`: Enable anti-detection measures (default: True)
- `human_delays`: Add human-like delays (default: True)
- `check_interval`: How often to check for messages (default: 300 seconds)

## Notes

- The system uses advanced anti-detection measures to avoid being blocked by Zillow
- All responses are automatically personalized with the prospect's name
- The system maintains a history of all processed messages
- Make sure your Zillow credentials are correct before processing messages
