# ⚙️ Configuration Reference

## Quick Setup Checklist

- [ ] Meta Developer Account created
- [ ] Business App created with WhatsApp
- [ ] Phone Number ID obtained
- [ ] Access Token obtained (temp or permanent)
- [ ] App Secret obtained
- [ ] Gemini API Key obtained
- [ ] .env file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Flask app running (`python run.py`)
- [ ] Ngrok tunnel started (`ngrok http 8000`)
- [ ] Webhook configured in Meta App
- [ ] Test message sent and received

---

## Configuration File Template (.env)

```properties
# =============================================================================
# WHATSAPP BUSINESS API CONFIGURATION
# =============================================================================

# ACCESS TOKEN
# Where to get: Meta App Dashboard → WhatsApp → API Setup → Temporary Access Token
# Note: Temp tokens expire in 24 hours. For production, use System User token.
# Docs: https://business.facebook.com/settings/system-users
ACCESS_TOKEN="YOUR_ACCESS_TOKEN_HERE"

# PHONE NUMBER ID
# Where to get: Meta App Dashboard → WhatsApp → API Setup
# This is the ID of your WhatsApp Business phone number
PHONE_NUMBER_ID="YOUR_PHONE_NUMBER_ID"

# RECIPIENT WAID (WhatsApp ID)
# This is where the bot will send replies
# Format: +[country_code][phone_number] (e.g., +923076053909)
RECIPIENT_WAID="+YOUR_PHONE_NUMBER"

# API VERSION
# Current stable version (update as needed)
VERSION="v23.0"

# =============================================================================
# META APP CONFIGURATION
# =============================================================================

# APP ID
# Where to get: Meta App Dashboard → Settings → Basic
APP_ID="YOUR_APP_ID"

# APP SECRET
# Where to get: Meta App Dashboard → Settings → Basic → Show App Secret
# Used for: Webhook signature validation
# Security: NEVER commit this to Git!
APP_SECRET="YOUR_APP_SECRET"

# VERIFY TOKEN
# This is a custom string YOU create
# Used for: Webhook verification when setting up webhook in Meta App
# Can be any string (e.g., "my_secure_verify_token_123")
VERIFY_TOKEN="YOUR_CUSTOM_VERIFY_TOKEN"

# =============================================================================
# AI SERVICES
# =============================================================================

# GEMINI API KEY (Current Implementation)
# Where to get: https://aistudio.google.com/app/apikey
# Used for: AI-powered responses with RAG
# Free tier: 60 requests/minute
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

# OPENAI CONFIGURATION (Optional - Alternative to Gemini)
# Where to get: https://platform.openai.com/api-keys
# Note: Currently not used, but available if you want to switch back
OPENAI_API_KEY=""
OPENAI_ASSISTANT_ID=""
```

---

## Environment-Specific Configurations

### Development (.env.development)
```properties
# Local development settings
ACCESS_TOKEN="temp_24h_token"
RECIPIENT_WAID="+your_test_number"
VERIFY_TOKEN="dev_verify_token"
GEMINI_API_KEY="your_dev_gemini_key"
```

### Production (.env.production)
```properties
# Production settings
ACCESS_TOKEN="permanent_system_user_token"
RECIPIENT_WAID="+production_number"
VERIFY_TOKEN="secure_production_token_xyz"
GEMINI_API_KEY="production_gemini_key"
```

---

## Application Configuration (app/config.py)

Current implementation loads from .env:

```python
def load_configurations(app):
    load_dotenv()
    
    # WhatsApp API
    app.config["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
    app.config["PHONE_NUMBER_ID"] = os.getenv("PHONE_NUMBER_ID")
    app.config["RECIPIENT_WAID"] = os.getenv("RECIPIENT_WAID")
    app.config["VERSION"] = os.getenv("VERSION")
    
    # Meta App
    app.config["APP_ID"] = os.getenv("APP_ID")
    app.config["APP_SECRET"] = os.getenv("APP_SECRET")
    app.config["VERIFY_TOKEN"] = os.getenv("VERIFY_TOKEN")
```

---

## Service Configuration

### Gemini AI (app/services/gemini_service.py)

```python
# Model Configuration
model_name = "gemini-2.5-flash"  # Fast, efficient model

generation_config = {
    "temperature": 1,              # Randomness (0=deterministic, 2=creative)
    "top_p": 0.95,                # Nucleus sampling threshold
    "top_k": 40,                  # Top-k sampling limit
    "max_output_tokens": 8192     # Maximum response length
}
```

**Available Models**:
- `gemini-2.5-flash` (current) - Fast, good quality
- `gemini-2.5-pro` - Better quality, slower
- `gemini-flash-latest` - Always latest flash version

### RAG Configuration (app/services/rag_service.py)

```python
# Document Processing
chunk_size = 500        # Words per chunk
overlap = 50           # Overlapping words between chunks
n_results = 3          # Number of contexts to retrieve

# Embedding Model
model = "all-MiniLM-L6-v2"  # 384-dimensional embeddings

# Vector Database
database = "ChromaDB"
storage = "./chroma_db/"
similarity = "cosine"
```

### Flask Server (run.py)

```python
# Development
app.run(
    host="0.0.0.0",     # Listen on all interfaces
    port=8000,          # Port number
    debug=True          # Enable debug mode (auto-reload)
)

# Production (use Gunicorn instead)
# gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## Webhook Configuration

### Meta App Dashboard Setup

1. **Navigate to**: Your Meta App → WhatsApp → Configuration

2. **Webhook Settings**:
   ```
   Callback URL: https://your-domain.com/webhook
   Verify Token: [Match your VERIFY_TOKEN from .env]
   ```

3. **Webhook Fields** (Subscribe to):
   - ✅ messages
   - ⬜ message_status (optional)
   - ⬜ message_echoes (optional)

4. **Test Webhook**:
   - Send test message from WhatsApp
   - Check Flask logs for incoming request
   - Verify signature validation passes

---

## Database Configuration

### ChromaDB (Vector Database)

```python
# Location
path = "./chroma_db/"

# Collection
name = "airbnb_docs"
distance_metric = "cosine"

# Persistence
mode = "persistent"  # Data survives restarts
```

**Maintenance**:
```bash
# View database size
du -sh chroma_db/

# Reset database (reindex all documents)
rm -rf chroma_db/

# Backup database
tar -czf chroma_backup.tar.gz chroma_db/
```

### Shelve DB (Chat History)

```python
# Files
chats_db.bak  # Backup
chats_db.dat  # Data
chats_db.dir  # Index

# Storage per user
wa_id → [conversation_history]
```

**Maintenance**:
```python
# View chat history
import shelve
with shelve.open("chats_db") as db:
    print(dict(db))

# Clear chat history
import shelve
with shelve.open("chats_db", writeback=True) as db:
    db.clear()

# Delete specific user
with shelve.open("chats_db", writeback=True) as db:
    del db["923076053909"]
```

---

## Logging Configuration

### Current Setup (app/config.py)

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
```

### Enhanced Production Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# File handler with rotation
handler = RotatingFileHandler(
    'whatsapp_bot.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
```

**Log Levels**:
- `DEBUG`: Detailed diagnostic info
- `INFO`: General informational messages (current)
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical failures

---

## Performance Tuning

### Flask

```python
# Use production WSGI server
# gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 run:app

# Workers: (2 × CPU cores) + 1
# Timeout: Adjust for AI response time
```

### RAG

```python
# Reduce chunk retrieval for faster responses
n_results = 2  # Instead of 3

# Use smaller embedding model (faster, less accurate)
model = "all-MiniLM-L6-v2"  # Current (good balance)
# model = "paraphrase-MiniLM-L3-v2"  # Faster, less accurate
```

### Gemini

```python
# Use faster model
model = "gemini-2.5-flash"  # Current
# model = "gemini-flash-latest"  # Always latest

# Reduce max tokens for faster responses
max_output_tokens = 2048  # Instead of 8192
```

---

## Security Configuration

### Signature Validation

**Enabled** (Production):
```python
# app/views.py
@webhook_blueprint.route("/webhook", methods=["POST"])
@signature_required  # ✅ Enabled
def webhook_post():
    return handle_message()
```

**Disabled** (Local Testing Only):
```python
@webhook_blueprint.route("/webhook", methods=["POST"])
# @signature_required  # ⚠️ Disabled for testing
def webhook_post():
    return handle_message()
```

### HTTPS Requirement

Meta requires HTTPS for webhooks:
- **Development**: Use ngrok (automatic HTTPS)
- **Production**: Use Let's Encrypt, Cloudflare, or cloud provider SSL

### Environment Variables Security

```bash
# Never commit .env to Git
echo ".env" >> .gitignore

# Use environment variables in production
export ACCESS_TOKEN="your_token"
export GEMINI_API_KEY="your_key"
```

---

## Deployment Configurations

### Heroku (Procfile)

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app --timeout 120
```

### Docker (Dockerfile)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

### Systemd (Linux Service)

```ini
[Unit]
Description=WhatsApp Bot
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/whatsapp-bot
Environment="PATH=/var/www/whatsapp-bot/venv/bin"
ExecStart=/var/www/whatsapp-bot/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 run:app

[Install]
WantedBy=multi-user.target
```

---

## Testing Configuration

### Unit Tests

```python
# test_config.py
import unittest
from app import create_app

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_config_loaded(self):
        self.assertIsNotNone(self.app.config['ACCESS_TOKEN'])
```

### Integration Tests

```python
# test_webhook.py
def test_webhook_verification():
    response = client.get(
        '/webhook?hub.mode=subscribe&hub.verify_token=123&hub.challenge=test'
    )
    assert response.status_code == 200
    assert response.data == b'test'
```

---

## Monitoring & Alerts

### Health Check Endpoint

Add to `app/views.py`:

```python
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chroma_documents": rag.collection.count(),
        "active_chats": len(list(shelve.open("chats_db")))
    })
```

### Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

Ping `/health` every 5 minutes

---

## Backup & Recovery

### Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup databases
cp -r chroma_db/ $BACKUP_DIR/
cp chats_db.* $BACKUP_DIR/

# Backup config (without secrets)
cp requirements.txt $BACKUP_DIR/
cp -r app/ $BACKUP_DIR/

echo "Backup created: $BACKUP_DIR"
```

### Recovery

```bash
# Restore from backup
tar -xzf backup_20251004.tar.gz
mv backup_20251004/chroma_db ./
mv backup_20251004/chats_db.* ./
```

---

**Configuration Version**: 2.0
**Last Updated**: October 4, 2025
