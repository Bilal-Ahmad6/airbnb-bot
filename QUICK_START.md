# 🚀 Quick Start Guide

## For Complete Beginners

This guide will get your WhatsApp AI bot running in 15 minutes.

---

## 📋 Prerequisites

✅ Python 3.8+ installed  
✅ WhatsApp Business account  
✅ Credit card (for Meta verification - no charges)  

---

## Step 1: Clone & Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/daveebbelaar/python-whatsapp-bot.git
cd python-whatsapp-bot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Get Meta Credentials (5 minutes)

### 2.1 Create Meta App

1. Go to https://developers.facebook.com/
2. Click **"My Apps"** → **"Create App"**
3. Choose **"Business"** → **"Next"**
4. Fill in:
   - App Name: "My WhatsApp Bot"
   - Contact Email: your email
5. Click **"Create App"**

### 2.2 Add WhatsApp Product

1. In your app dashboard, find **"WhatsApp"**
2. Click **"Set Up"**
3. Follow the wizard

### 2.3 Get Phone Number ID & Token

1. Go to **WhatsApp** → **API Setup**
2. Copy these values:

```
Temporary Access Token: EAAJ... (long string)
Phone Number ID: 123456789... (numbers)
```

3. Click **"Add recipient"** → Enter YOUR WhatsApp number
4. Verify the code you receive

### 2.4 Get App ID & Secret

1. Go to **Settings** → **Basic**
2. Copy:
   ```
   App ID: 1234567890
   ```
3. Click **"Show"** next to App Secret:
   ```
   App Secret: abc123def456...
   ```

---

## Step 3: Get Gemini API Key (2 minutes)

1. Go to https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

---

## Step 4: Configure .env File (2 minutes)

1. Copy the example:
   ```bash
   cp .env.example .env  # Or create new .env file
   ```

2. Edit `.env` with your values:

```properties
# Paste your values here
ACCESS_TOKEN="EAAJ..."                    # From Step 2.3
PHONE_NUMBER_ID="123456789"               # From Step 2.3
RECIPIENT_WAID="+1234567890"             # YOUR WhatsApp number
VERSION="v23.0"

APP_ID="1234567890"                      # From Step 2.4
APP_SECRET="abc123..."                   # From Step 2.4
VERIFY_TOKEN="my_secret_token_123"       # You create this (any string)

GEMINI_API_KEY="AIza..."                 # From Step 3

# Leave these empty for now
OPENAI_API_KEY=""
OPENAI_ASSISTANT_ID=""
```

**Save the file!**

---

## Step 5: Start the Bot (1 minute)

```bash
# Start Flask server
python run.py
```

You should see:
```
2025-10-04 08:00:00,000 - INFO - Flask app started
2025-10-04 08:00:00,000 - INFO - Registered routes: [..., '/webhook', '/']
 * Running on http://127.0.0.1:8000
```

✅ **Bot is running locally!**

---

## Step 6: Expose with Ngrok (2 minutes)

Your bot needs a public URL for Meta to send messages.

### 6.1 Install Ngrok

- Download from https://ngrok.com/download
- Extract and add to PATH

### 6.2 Start Ngrok

Open a **NEW terminal** (keep Flask running):

```bash
ngrok http 8000
```

You'll see:
```
Forwarding  https://abc123def.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123def.ngrok.io`)

---

## Step 7: Configure Webhook (3 minutes)

### 7.1 In Meta App Dashboard

1. Go to **WhatsApp** → **Configuration**
2. Under **"Webhook"**, click **"Edit"**
3. Fill in:

```
Callback URL: https://abc123def.ngrok.io/webhook
Verify Token: my_secret_token_123
```
(Use YOUR ngrok URL and the VERIFY_TOKEN from .env)

4. Click **"Verify and Save"**

✅ Should show **"Verified"**

### 7.2 Subscribe to Webhook Fields

1. Click **"Manage"** under Webhook Fields
2. Check ✅ **messages**
3. Click **"Save"**

---

## Step 8: Test Your Bot! 🎉

### Send a Test Message

1. Open WhatsApp on your phone
2. Send a message to the **test number** (shown in Meta dashboard)
3. Type: `Hello!`

### Expected Result

✅ You should receive a reply from the bot!

### Check Logs

In your Flask terminal, you should see:
```
2025-10-04 08:00:00,000 - INFO - ✅ Valid WhatsApp message. Processing...
2025-10-04 08:00:00,000 - INFO - 📩 Message from YourName (1234567890): Hello!
2025-10-04 08:00:00,000 - INFO - 📤 Sending reply to +1234567890: ...
```

---

## 🎯 What Just Happened?

```
You (WhatsApp) → Meta Cloud API → Your Webhook → Flask
                                                    ↓
                                           RAG retrieves context
                                                    ↓
                                           Gemini generates response
                                                    ↓
Meta Cloud API ← Your Flask App ← Formatted message
        ↓
You (WhatsApp) ← AI Response!
```

---

## 🔧 Common Issues

### ❌ "Webhook verification failed"

**Problem**: VERIFY_TOKEN doesn't match  
**Solution**: Make sure VERIFY_TOKEN in .env matches what you entered in Meta dashboard

---

### ❌ "401 Unauthorized"

**Problem**: ACCESS_TOKEN expired (24 hours)  
**Solution**: 
1. Go to Meta App → WhatsApp → API Setup
2. Copy new Temporary Access Token
3. Update ACCESS_TOKEN in .env
4. Restart Flask (`Ctrl+C`, then `python run.py`)

---

### ❌ "No response from bot"

**Check**:
1. Flask is running (`python run.py`)
2. Ngrok is running (`ngrok http 8000`)
3. Webhook is verified in Meta dashboard
4. You're sending from the verified phone number

---

### ❌ "Module not found"

**Solution**:
```bash
pip install -r requirements.txt
```

---

## 📚 Next Steps

Now that your bot is working:

1. **Add Knowledge Base**
   - Add PDF files to `data/` folder
   - Restart Flask - it will automatically index them
   - Ask questions based on PDF content!

2. **Customize Responses**
   - Edit `app/services/gemini_service.py`
   - Change the system prompt to match your use case

3. **Deploy to Production**
   - Get permanent access token (instead of 24h temp)
   - Deploy to Heroku/AWS/DigitalOcean
   - Use custom domain instead of ngrok

4. **Read Full Documentation**
   - `SYSTEM_DOCUMENTATION.md` - Complete system overview
   - `CONFIGURATION.md` - All configuration options
   - `docs/RAG_SYSTEM.md` - How RAG works

---

## 🆘 Need Help?

1. Check **SYSTEM_DOCUMENTATION.md** for detailed explanations
2. Check Flask logs for error messages
3. Check Meta App Dashboard for webhook errors
4. Verify all credentials in `.env` are correct

---

## ✅ Success Checklist

- [ ] Flask app running without errors
- [ ] Ngrok showing forwarding URL
- [ ] Webhook verified in Meta dashboard
- [ ] Test message sent from WhatsApp
- [ ] Response received from bot
- [ ] Flask logs showing message processing

**Congratulations! Your WhatsApp AI Bot is live! 🎉**

---

## 🎓 Understanding the Code

### Main Files to Know

1. **`run.py`** - Starts the Flask server
2. **`app/views.py`** - Receives WhatsApp webhooks
3. **`app/services/gemini_service.py`** - AI responses
4. **`app/services/rag_service.py`** - PDF knowledge base
5. **`app/utils/whatsapp_utils.py`** - Message handling

### Message Flow

```python
# 1. Message arrives
POST /webhook → views.py

# 2. Extract data
wa_id, name, message = extract_from_webhook(body)

# 3. Get context
context = rag.retrieve_context(message)

# 4. Generate response
response = gemini.generate(message + context)

# 5. Send reply
send_to_whatsapp(recipient, response)
```

### Customization Examples

**Change bot personality**:
```python
# app/services/gemini_service.py, line ~55
system_message = "You are a funny, sarcastic assistant..."
```

**Change response format**:
```python
# app/utils/whatsapp_utils.py
response = f"🤖 Bot says: {response}"
```

**Reply to sender instead of fixed number**:
```python
# app/utils/whatsapp_utils.py, line ~95
data = get_text_message_input(wa_id, response)  # Instead of RECIPIENT_WAID
```

---

**Quick Start Guide Version**: 1.0  
**Last Updated**: October 4, 2025

**Ready to build something amazing? Let's go! 🚀**
