# AI Email Assistant - Technical Assessment

## 🎯 Overview
A professional AI-powered email assistant built using the **Google Agent Development Kit (ADK)**. This agent automates Gmail workflows including searching for emails, retrieving full content, and drafting responses with a strict **Human-in-the-Loop** approval process.

## 🏗️ Technical Stack
*   **Framework**: Google ADK (Agent Development Kit)
*   **LLM**: OpenAI GPT-4o (via LiteLLM)
*   **Integration**: Gmail API (OAuth2)
*   **Environment**: Python 3.12+

## ✅ Features Implemented
*   **Email Search**: Search for emails using subjects or keywords.
*   **Email Detail Retrieval**: Extracts Sender, Subject, and full Body content.
*   **Draft Generation**: Automatically generates contextual, professional replies.
*   **Human-in-the-Loop**: The agent presents drafts and waits for explicit user approval before sending.
*   **Secure Sending**: Real implementation of Gmail API 'send' functionality.

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.9+
*   Google Cloud Project with Gmail API enabled.

### 2. Configuration
Create a `.env` file in the root directory:
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o

# Google Gmail API
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
GOOGLE_SCOPES=https://mail.google.com/
```

Place your `credentials.json` (downloaded from Google Cloud Console) in the project root.

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python3 main.py
```
On the first run, it will open a browser for Google OAuth authentication.

## 🛡️ Security & Privacy
*   **OAuth2**: Uses secure refresh token rotation.
*   **No Hardcoding**: All secrets are managed via environment variables.
*   **Explicit Consent**: The agent is programmed to never send an email without user confirmation.

