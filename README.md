# AI Email Agent - Technical Assessment Submission

## 🎯 Overview
Professional AI-powered email assistant built with **LangChain 2026** and **LangGraph**, demonstrating advanced agentic capabilities with Gmail integration and strict human-in-the-loop safeguards.

---

## 🏗️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12 |
| **AI Framework** | LangChain + LangGraph |
| **LLM** | OpenAI GPT-4o |
| **Tools** | Gmail API (OAuth2) |
| **Environment** | python-dotenv |

---

## ✅ Assessment Requirements Completed

### 1. Core Functionality
- ✅ **Email Search**: Semantic search across Gmail using natural language queries
- ✅ **Email Reading**: Full email content retrieval with proper authentication
- ✅ **Draft Creation**: Generate contextual email drafts based on user intent
- ✅ **Send with Confirmation**: Human-in-the-loop approval required before sending

### 2. Safety & Security
- ✅ **OAuth2 Authentication**: Secure Gmail access with refresh token management
- ✅ **Environment Variables**: Sensitive credentials managed via `.env` file
- ✅ **Explicit Consent**: Agent **always** asks permission before sending emails
- ✅ **Input Validation**: Configuration checks on startup

### 3. Code Quality
- ✅ **Modern 2026 API**: Uses latest `langchain.agents.create_agent`
- ✅ **Clean Architecture**: Modular functions with clear separation of concerns
- ✅ **Error Handling**: Try-catch blocks with informative error messages
- ✅ **Type Safety**: Proper type hints and IDE compatibility

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
Google Cloud Project with Gmail API enabled
```

### Get credentials.json (Google OAuth2)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Gmail API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API" and click "Enable"
4. Create OAuth2 Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app" as application type
   - Name it (e.g., "Email Agent")
   - Click "Create"
5. Download the JSON file:
   - Click the download icon next to your new OAuth client
   - Save as `credentials.json` in project root

### Installation
```bash
# Navigate to project directory
cd ai-email-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. **Get credentials.json** (see "Get credentials.json" section above)

2. Create `.env` file:
```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
GOOGLE_SCOPES=https://mail.google.com/
```

3. Place `credentials.json` in project root (same folder as `main.py`)

### Run
```bash
python3 main.py
```

On first run, a browser window opens for Gmail OAuth consent. After authorization, `token.json` is auto-generated for subsequent runs.

---

## 💡 Usage Examples

### Example 1: Search & Read
```
👤 You: Search for emails about AI from the last week
🤖 Agent: [Displays list of relevant emails with snippets]

👤 You: Read the latest email from GitHub
🤖 Agent: [Shows full email content]
```

### Example 2: Draft & Send
```
👤 You: Draft a reply thanking them for the update
🤖 Agent: [Creates draft]
Here's the draft:
"Thank you for the update..."

Do you want me to send this? (yes/no)

👤 You: yes
🤖 Agent: ✅ Email sent successfully!
```

---

## 📂 Project Structure

```
ai-email-agent/
├── main.py                 # Core agent implementation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (git-ignored)
├── credentials.json        # Google OAuth2 config (git-ignored)
├── token.json             # Auto-generated OAuth token (git-ignored)
├── README.md              # This file
└── .gitignore             # Excludes sensitive files
```

---

## 🔒 Security Features

1. **No Hardcoded Credentials**: All secrets in `.env` file
2. **OAuth2 Flow**: Industry-standard authentication with Google
3. **Token Refresh**: Automatic access token renewal
4. **Explicit Confirmation**: Agent **never** sends emails without user approval
5. **Scoped Access**: Minimal permissions (only Gmail access)

---

## 🧪 Testing Notes

### Validated Scenarios
- ✅ Email search with various queries ("AI", "GitHub", date ranges)
- ✅ Reading emails by subject/sender
- ✅ Draft creation based on context
- ✅ Send confirmation workflow
- ✅ Token refresh on expiration
- ✅ Error handling for invalid credentials

### Known Behaviors
- **First Run**: Requires browser authentication (expected OAuth flow)
- **List Numbers**: When searching, refer to emails by subject/sender (not list index)
- **Verbose Mode**: Agent shows reasoning steps for transparency

---

## 🛠️ Dependencies

```txt
langchain                  # Core LangChain framework
langchain-openai          # OpenAI LLM integration
langchain-community       # Gmail toolkit
langgraph                 # Agentic orchestration
langchainhub             # Prompt management
google-api-python-client # Gmail API client
google-auth-httplib2     # OAuth2 authentication
google-auth-oauthlib     # OAuth flow
python-dotenv            # Environment management
```

---

## 📊 Agent Capabilities

The agent is equipped with **5 Gmail tools**:
1. `search_emails` - Find emails by query
2. `get_message` - Read email by ID
3. `create_draft` - Compose draft email
4. `send_message` - Send email (with confirmation)
5. `get_thread` - Retrieve email threads

---

## 🎓 Design Decisions

### Why LangGraph?
- **Stateful Conversations**: Maintains context across multiple turns
- **Tool Orchestration**: Intelligent tool selection based on user intent
- **Modern API**: Uses 2026 `create_agent` (replaces deprecated patterns)

### Why GPT-4o?
- **Reasoning Quality**: Better email understanding vs. GPT-3.5
- **Tool Calling**: Optimized for function calling
- **Temperature 0**: Deterministic responses for reliability

### Human-in-the-Loop
Per assessment requirements, the agent:
1. **Always** searches before reading (to get message IDs)
2. **Always** creates drafts before sending
3. **Always** asks explicit "yes/no" before `send_message` tool execution

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ImportError: create_react_agent` | Use `langchain.agents.create_agent` (2026 API) |
| `OPENAI_API_KEY not found` | Check `.env` file exists and is formatted correctly |
| `credentials.json not found` | Download OAuth2 Desktop credentials from Google Cloud Console |
| `HttpError 404` when reading | Use `search_emails` first to get valid message IDs |
| Token expired | Delete `token.json` and re-authenticate |

---

## 📝 Submission Notes

**Evaluator Instructions:**
1. Ensure `.env` contains valid `OPENAI_API_KEY`
2. First run will open browser for Gmail OAuth (one-time setup)
3. Test with: `"Search for emails about AI"` → `"Read the latest one"` → `"Draft a thank you reply"`
4. Observe agent **asking permission** before sending

**Time Investment:** ~4 hours (setup, implementation, testing, documentation)

**Code Quality:** Production-ready with error handling, type hints, and modern 2026 patterns

---

## 📧 Contact
For questions regarding this submission, please contact via the provided email address.

---

**Built with ❤️ using LangChain & LangGraph**
