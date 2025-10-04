# Build AI WhatsApp Bots with Pure Python

This guide will walk you through the process of creating a WhatsApp bot using the Meta (formerly Facebook) Cloud API with pure Python and Flask. We integrate webhook events to receive messages in real-time and use **Google Gemini AI** with a **RAG (Retrieval-Augmented Generation) system** to generate intelligent responses. The bot also supports **voice messages** with transcription and text-to-speech capabilities using **UpliftAI**.

## 🚀 Features

- ✅ **Text Messages**: AI-powered responses using Google Gemini
- ✅ **Voice Messages**: Full voice-to-voice conversation support
- ✅ **RAG System**: Knowledge base integration with ChromaDB
- ✅ **Multi-language Support**: English, Urdu, Arabic, and more
- ✅ **WhatsApp Cloud API**: Official Meta integration
- ✅ **Webhook Security**: HMAC signature validation
- ✅ **Easy Deployment**: Flask-based architecture

## Prerequisites

1. A Meta developer account — If you don’t have one, you can [create a Meta developer account here](https://developers.facebook.com/).
2. A business app — If you don't have one, you can [learn to create a business app here](https://developers.facebook.com/docs/development/create-an-app/). If you don't see an option to create a business app, select **Other** > **Next** > **Business**.
3. Familiarity with Python to follow the tutorial.


## Table of Contents

- [Build AI WhatsApp Bots with Pure Python](#build-ai-whatsapp-bots-with-pure-python)
  - [Prerequisites](#prerequisites)
  - [Table of Contents](#table-of-contents)
  - [Get Started](#get-started)
  - [Step 1: Select Phone Numbers](#step-1-select-phone-numbers)
  - [Step 2: Send Messages with the API](#step-2-send-messages-with-the-api)
  - [Step 3: Configure Webhooks to Receive Messages](#step-3-configure-webhooks-to-receive-messages)
      - [Start your app](#start-your-app)
      - [Launch ngrok](#launch-ngrok)
      - [Integrate WhatsApp](#integrate-whatsapp)
      - [Testing the Integration](#testing-the-integration)
  - [Step 4: Understanding Webhook Security](#step-4-understanding-webhook-security)
      - [Verification Requests](#verification-requests)
      - [Validating Verification Requests](#validating-verification-requests)
      - [Validating Payloads](#validating-payloads)
  - [Step 5: Learn about the API and Build Your App](#step-5-learn-about-the-api-and-build-your-app)
  - [Step 6: Integrate AI into the Application](#step-6-integrate-ai-into-the-application)
  - [Step 7: Voice Message Integration](#step-7-voice-message-integration)
  - [Step 8: Add a Phone Number](#step-8-add-a-phone-number)
  - [Documentation](#documentation)
  - [Datalumina](#datalumina)
  - [Tutorials](#tutorials)

## Get Started

1. **Overview & Setup**: Begin your journey [here](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started).
2. **Locate Your Bots**: Your bots can be found [here](https://developers.facebook.com/apps/).
3. **WhatsApp API Documentation**: Familiarize yourself with the [official documentation](https://developers.facebook.com/docs/whatsapp).
4. **Helpful Guide**: Here's a [Python-based guide](https://developers.facebook.com/blog/post/2022/10/24/sending-messages-with-whatsapp-in-your-python-applications/) for sending messages.
5. **API Docs for Sending Messages**: Check out [this documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages).

## Step 1: Select Phone Numbers

- Make sure WhatsApp is added to your App.
- You begin with a test number that you can use to send messages to up to 5 numbers.
- Go to API Setup and locate the test number from which you will be sending messages.
- Here, you can also add numbers to send messages to. Enter your **own WhatsApp number**.
- You will receive a code on your phone via WhatsApp to verify your number.

## Step 2: Send Messages with the API

1. Obtain a 24-hour access token from the API access section.
2. It will show an example of how to send messages using a `curl` command which can be send from the terminal or with a tool like Postman.
3. Let's convert that into a [Python function with the request library](https://github.com/daveebbelaar/python-whatsapp-bot/blob/main/start/whatsapp_quickstart.py).
4. Create a `.env` files based on `example.env` and update the required variables. [Video example here](https://www.youtube.com/watch?v=sOwG0bw0RNU).
5. You will receive a "Hello World" message (Expect a 60-120 second delay for the message).

Creating an access that works longer then 24 hours
1. Create a [system user at the Meta Business account level](https://business.facebook.com/settings/system-users).
2. On the System Users page, configure the assets for your System User, assigning your WhatsApp app with full control. Don't forget to click the Save Changes button.
   - [See step 1 here](https://github.com/daveebbelaar/python-whatsapp-bot/blob/main/img/meta-business-system-user-token.png)
   - [See step 2 here](https://github.com/daveebbelaar/python-whatsapp-bot/blob/main/img/adding-assets-to-system-user.png)
3. Now click `Generate new token` and select the app, and then choose how long the access token will be valid. You can choose 60 days or never expire.
4. Select all the permissions, as I was running into errors when I only selected the WhatsApp ones.
5. Confirm and copy the access token.

Now we have to find the following information on the **App Dashboard**:

- **APP_ID**: "<YOUR-WHATSAPP-BUSINESS-APP_ID>" (Found at App Dashboard)
- **APP_SECRET**: "<YOUR-WHATSAPP-BUSINESS-APP_SECRET>" (Found at App Dashboard)
- **RECIPIENT_WAID**: "<YOUR-RECIPIENT-TEST-PHONE-NUMBER>" (This is your WhatsApp ID, i.e., phone number. Make sure it is added to the account as shown in the example test message.)
- **VERSION**: "v18.0" (The latest version of the Meta Graph API)
- **ACCESS_TOKEN**: "<YOUR-SYSTEM-USER-ACCESS-TOKEN>" (Created in the previous step)

> You can only send a template type message as your first message to a user. That's why you have to send a reply first before we continue. Took me 2 hours to figure this out.


## Step 3: Configure Webhooks to Receive Messages

> Please note, this is the hardest part of this tutorial.

#### Start your app
- Make you have a python installation or environment and install the requirements: `pip install -r requirements.txt`
- Run your Flask app locally by executing [run.py](https://github.com/daveebbelaar/python-whatsapp-bot/blob/main/run.py)

#### Launch ngrok

The steps below are taken from the [ngrok documentation](https://ngrok.com/docs/integrations/whatsapp/webhooks/).

> You need a static ngrok domain because Meta validates your ngrok domain and certificate!

Once your app is running successfully on localhost, let's get it on the internet securely using ngrok!

1. If you're not an ngrok user yet, just sign up for ngrok for free.
2. Download the ngrok agent.
3. Go to the ngrok dashboard, click Your [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken), and copy your Authtoken.
4. Follow the instructions to authenticate your ngrok agent. You only have to do this once.
5. On the left menu, expand Cloud Edge and then click Domains.
6. On the Domains page, click + Create Domain or + New Domain. (here everyone can start with [one free domain](https://ngrok.com/blog-post/free-static-domains-ngrok-users))
7. Start ngrok by running the following command in a terminal on your local desktop:
```
ngrok http 8000 --domain your-domain.ngrok-free.app
```
8. ngrok will display a URL where your localhost application is exposed to the internet (copy this URL for use with Meta).


#### Integrate WhatsApp

In the Meta App Dashboard, go to WhatsApp > Configuration, then click the Edit button.
1. In the Edit webhook's callback URL popup, enter the URL provided by the ngrok agent to expose your application to the internet in the Callback URL field, with /webhook at the end (i.e. https://myexample.ngrok-free.app/webhook).
2. Enter a verification token. This string is set up by you when you create your webhook endpoint. You can pick any string you like. Make sure to update this in your `VERIFY_TOKEN` environment variable.
3. After you add a webhook to WhatsApp, WhatsApp will submit a validation post request to your application through ngrok. Confirm your localhost app receives the validation get request and logs `WEBHOOK_VERIFIED` in the terminal.
4. Back to the Configuration page, click Manage.
5. On the Webhook fields popup, click Subscribe to the **messages** field. Tip: You can subscribe to multiple fields.
6. If your Flask app and ngrok are running, you can click on "Test" next to messages to test the subscription. You recieve a test message in upper case. If that is the case, your webhook is set up correctly.


#### Testing the Integration
Use the phone number associated to your WhatsApp product or use the test number you copied before.
1. Add this number to your WhatsApp app contacts and then send a message to this number.
2. Confirm your localhost app receives a message and logs both headers and body in the terminal.
3. Test if the bot replies back to you in upper case.
4. You have now succesfully integrated the bot! 🎉
5. Now it's time to acutally build cool things with this.


## Step 4: Understanding Webhook Security

Below is some information from the Meta Webhooks API docs about verification and security. It is already implemented in the code, but you can reference it to get a better understanding of what's going on in [security.py](https://github.com/daveebbelaar/python-whatsapp-bot/blob/main/app/decorators/security.py)

#### Verification Requests

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=process%20these%20requests.-,Verification%20Requests,-Anytime%20you%20configure)

Anytime you configure the Webhooks product in your App Dashboard, we'll send a GET request to your endpoint URL. Verification requests include the following query string parameters, appended to the end of your endpoint URL. They will look something like this:

```
GET https://www.your-clever-domain-name.com/webhook?
  hub.mode=subscribe&
  hub.challenge=1158201444&
  hub.verify_token=meatyhamhock
```

The verify_token, `meatyhamhock` in the case of this example, is a string that you can pick. It doesn't matter what it is as long as you store in the `VERIFY_TOKEN` environment variable.

#### Validating Verification Requests

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=Validating%20Verification%20Requests)

Whenever your endpoint receives a verification request, it must:
- Verify that the hub.verify_token value matches the string you set in the Verify Token field when you configure the Webhooks product in your App Dashboard (you haven't set up this token string yet).
- Respond with the hub.challenge value.

#### Validating Payloads

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=int-,Validating%20Payloads,-We%20sign%20all)

WhatsApp signs all Event Notification payloads with a SHA256 signature and include the signature in the request's X-Hub-Signature-256 header, preceded with sha256=. You don't have to validate the payload, but you should.

To validate the payload:
- Generate a SHA256 signature using the payload and your app's App Secret.
- Compare your signature to the signature in the X-Hub-Signature-256 header (everything after sha256=). If the signatures match, the payload is genuine.


## Step 5: Learn about the API and Build Your App

Review the developer documentation to learn how to build your app and start sending messages. [See documentation](https://developers.facebook.com/docs/whatsapp/cloud-api).

## Step 6: Integrate AI into the Application

This bot uses **Google Gemini AI** with a **RAG (Retrieval-Augmented Generation)** system for intelligent responses.

### Features:
- **Google Gemini 2.5 Flash**: Fast, accurate AI responses
- **RAG System**: ChromaDB vector database for knowledge retrieval
- **PDF Knowledge Base**: Automatically processes PDFs in `/data` folder
- **Chat History**: Maintains conversation context per user
- **Multi-language**: Supports English, Urdu, Arabic, and more

### Setup:
1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GEMINI_API_KEY="your-key-here"`
3. Add PDF documents to the `/data` folder
4. The RAG system automatically processes and indexes them

### Configuration:
See `app/services/gemini_service.py` for AI configuration and `app/services/rag_service.py` for RAG settings.

## Step 7: Voice Message Integration

The bot supports **full voice message capabilities** - responding to voice with voice, and text with text.

### 🎤 Voice Features:
- **Voice-to-Voice**: User sends voice → Bot replies with voice
- **Text-to-Text**: User sends text → Bot replies with text
- **Transcription**: Converts voice to text using Gemini
- **Text-to-Speech**: Converts AI responses to voice using UpliftAI
- **Multi-language**: Supports Urdu, English, Arabic voices

### Setup Voice Messages:

#### 1. Get UpliftAI API Key
1. Visit [UpliftAI](https://upliftai.org)
2. Sign up and get your API key
3. Add to `.env`:
```bash
UPLIFTAI_API_KEY="your-upliftai-api-key"
UPLIFTAI_VOICE_ID="v_8eelc901"  # Urdu female voice
UPLIFTAI_OUTPUT_FORMAT="MP3_22050_64"  # Optimized for WhatsApp
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Test Voice Functionality
```bash
python test_voice.py
```

#### 4. Send a Voice Message
Send a voice message to your WhatsApp bot and receive a voice reply!

### How It Works:

**Voice Message Flow:**
```
User sends voice
    ↓
Download from WhatsApp
    ↓
Transcribe to text (Gemini)
    ↓
Process with AI + RAG (Gemini)
    ↓
Convert to speech (UpliftAI)
    ↓
Send voice reply
```

**Text Message Flow:**
```
User sends text
    ↓
Process with AI + RAG (Gemini)
    ↓
Send text reply
```

### Voice Configuration:

Available voice IDs in `.env`:
```bash
# Urdu Voices
UPLIFTAI_VOICE_ID="v_8eelc901"        # Female (default)
UPLIFTAI_VOICE_ID="v_urdu_male_01"    # Male

# English Voices
UPLIFTAI_VOICE_ID="v_en_us_female_01" # US Female
UPLIFTAI_VOICE_ID="v_en_us_male_01"   # US Male
```

### Documentation:
- **Quick Reference**: See `VOICE_QUICKREF.md` for quick setup
- **Full Integration Guide**: See `docs/VOICE_INTEGRATION.md`
- **API Documentation**: See `docs/VOICE_HANDLER.md`

## Step 8: Add a Phone Number

When you’re ready to use your app for a production use case, you need to use your own phone number to send messages to your users.

To start sending messages to any WhatsApp number, add a phone number. To manage your account information and phone number, [see the Overview page.](https://business.facebook.com/wa/manage/home/) and the [WhatsApp docs](https://developers.facebook.com/docs/whatsapp/phone-numbers/).

If you want to use a number that is already being used in the WhatsApp customer or business app, you will have to fully migrate that number to the business platform. Once the number is migrated, you will lose access to the WhatsApp customer or business app. [See Migrate Existing WhatsApp Number to a Business Account for information](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/migrate-existing-whatsapp-number-to-a-business-account).

Once you have chosen your phone number, you have to add it to your WhatsApp Business Account. [See Add a Phone Number](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/add-a-phone-number).

When dealing with WhatsApp Business API and wanting to experiment without affecting your personal number, you have a few options:

1. Buy a New SIM Card
2. Virtual Phone Numbers
3. Dual SIM Phones
4. Use a Different Device
5. Temporary Number Services
6. Dedicated Devices for Development

**Recommendation**: If this is for a more prolonged or professional purpose, using a virtual phone number service or purchasing a new SIM card for a dedicated device is advisable. For quick tests, a temporary number might suffice, but always be cautious about security and privacy. Remember that once a number is associated with WhatsApp Business API, it cannot be used with regular WhatsApp on a device unless you deactivate it from the Business API and reverify it on the device.

## Documentation

### 📚 Complete Documentation
This repository includes comprehensive documentation for all features:

#### Main Documentation
- **[VOICE_QUICKREF.md](VOICE_QUICKREF.md)** - Quick reference for voice features
- **[docs/VOICE_INTEGRATION.md](docs/VOICE_INTEGRATION.md)** - Full voice integration guide
- **[docs/VOICE_HANDLER.md](docs/VOICE_HANDLER.md)** - Voice API documentation
- **[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)** - Complete documentation index

#### Core Features
- **AI Integration**: Google Gemini with RAG system
- **Voice Messages**: UpliftAI text-to-speech integration
- **WhatsApp API**: Meta Cloud API integration
- **Security**: HMAC signature validation
- **Deployment**: Flask application deployment

#### Testing
- **[test_voice.py](test_voice.py)** - Test voice functionality
- **[test_rag_simple.py](test_rag_simple.py)** - Test RAG system

### 🚀 Quick Start Summary

1. **Clone and Install**
   ```bash
   git clone <repository>
   cd python-whatsapp-bot
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Copy `example.env` to `.env`
   - Add your API keys (WhatsApp, Gemini, UpliftAI)
   - Update phone numbers

3. **Test Components**
   ```bash
   python test_voice.py  # Test voice features
   python run.py         # Start the bot
   ```

4. **Deploy**
   - Start ngrok tunnel
   - Configure WhatsApp webhook
   - Send messages to your bot!

## Datalumina

This document is provided to you by Datalumina. We help data analysts, engineers, and scientists launch and scale a successful freelance business — $100k+ /year, fun projects, happy clients. If you want to learn more about what we do, you can visit our [website](https://www.datalumina.com/) and subscribe to our [newsletter](https://www.datalumina.com/newsletter). Feel free to share this document with your data friends and colleagues.

## Tutorials
For video tutorials, visit the YouTube channel: [youtube.com/@daveebbelaar](https://www.youtube.com/@daveebbelaar).
