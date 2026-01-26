# AI Email Response Agent 🤖📧

This project implements an intelligent, agentic email assistant capable of searching Gmail, drafting context-aware responses using LLMs, and sending replies upon user approval.

## 🏗️ Architecture Design

As an **AI Solution Engineer**, I chose a hybrid "Agent-Client" architecture to simulate a production-ready environment:

* **The Brain (Backend - n8n):**
    * Leverages **LangChain** for agentic reasoning and tool orchestration.
    * Decouples the AI logic from the client, allowing for seamless model updates (e.g., swapping GPT-4 for Claude) without patching the client.
    * Manages state and conversation memory via a persistent session handler.
    * Uses a **ReAct** pattern (Reasoning + Acting) to determine when to search vs. when to draft.

* **The Interface (Client - Python):**
    * A lightweight CLI (Command Line Interface) that acts as the frontend.
    * Communicates with the backend via RESTful Webhooks.
    * Ensures a clean separation of concerns.

---

## 🚀 Setup & Installation

Since the requirement states the agent must be runnable using **your own Gmail credentials**, this solution is designed to run against a local n8n instance.

### Prerequisites
* **Python 3.x**
* **Node.js / npx** (To run n8n locally)
* **Google Cloud Console Project** (Enabled Gmail API + OAuth2 Credentials)
* **OpenAI API Key**

---

### Step 1: Backend Setup (n8n)

1.  **Start n8n locally:**
    Open your terminal and run:
    ```bash
    npx n8n start
    ```
    *Note: This will launch n8n at `http://localhost:5678`.*

2.  **Import the Workflow:**
    * Open `http://localhost:5678` in your browser.
    * Go to **Workflows** → **Import from File**.
    * Select the `agent_workflow.json` file provided in this zip.

3.  **Configure Credentials:**
    * **Gmail:** Open the Gmail nodes (Search/Get/Send) and create a new credential using your Google OAuth2 Client ID & Secret.
    * **OpenAI:** Open the "OpenAI Chat Model" node and input your API Key.

4.  **Activate the Agent:**
    * Toggle the workflow status to **Active** (Top right switch must be green).
    * **Crucial:** Ensure the **Chat Trigger** node has `Authentication` set to **None** to allow the Python script to connect.

---

### Step 2: Client Setup (Python)

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create Environment File (.env):**
    
    Create a `.env` file in the project root directory:
    
    **Option A: Quick setup with custom webhook URL (Recommended)**
    ```bash
    # One-liner: Copy template and set your custom webhook URL
    cp .env.example .env && read -p "Enter your n8n webhook URL: " webhook_url && echo "N8N_WEBHOOK_URL=${webhook_url}" > .env
    ```
    
    Or with a default URL:
    ```bash
    # Copy and initialize with default local URL
    cp .env.example .env && sed -i '' 's|http://localhost:5678/webhook/email-agent|http://localhost:5678/webhook/email-agent/chat|g' .env
    ```
    
    **Option B: Using the provided template (Manual edit)**
    ```bash
    # Copy the example file
    cp .env.example .env
    ```
    
    Then edit the `.env` file and update the webhook URL:
    ```env
    # n8n webhook URL (default for local development)
    N8N_WEBHOOK_URL=http://localhost:5678/webhook/email-agent/chat
    ```
    
    **Option C: Create from scratch**
    ```bash
    # Create a new .env file with default URL
    echo "N8N_WEBHOOK_URL=http://localhost:5678/webhook/email-agent/chat" > .env
    ```
    
    **Option D: Set as environment variable (temporary)**
    ```bash
    # For current terminal session only
    export N8N_WEBHOOK_URL=http://localhost:5678/webhook/email-agent/chat
    ```
    
    > **Note:** The `.env` file is already in `.gitignore` to protect your configuration from being committed to version control.

3.  **Verify Configuration:**
    The `main.py` script will automatically read the `N8N_WEBHOOK_URL` from your environment variables. If not set, it defaults to `http://localhost:5678/webhook/email-agent/chat`.

4.  **Run the Agent:**
    ```bash
    python main.py
    ```

---

## 🧪 Usage Example

Once the agent is running, you can interact with it naturally:

> **User:** "Find the email from Google about the AI Studio update."
> **Agent:** (Uses Search Tool) "I found an email titled 'Welcome to AI Studio'. Would you like me to draft a reply?"
> **User:** "Yes, say thanks and that I'm excited to test it."
> **Agent:** (Generates Draft) "Here is a draft... [Draft Content] ... Should I send it?"
> **User:** "Yes"
> **Agent:** (Uses Send Tool) "Reply sent successfully!"

---

## 📝 Assumptions & Decisions
1.  **Data Privacy:** The solution runs locally to ensure your OAuth tokens remain on your machine and are not shared.
2.  **Authentication:** For the purpose of this assessment, the webhook endpoint is open (Auth: None) to simplify local testing between the script and the engine. In production, this would be secured via Header Auth or API Keys.
3.  **Error Handling:** The agent is robust against "Email not found" errors and will ask for clarification instead of crashing.
# Qusaitr-n8n-email-agent-assigment
# Qusaitr-Qusaitr-n8n-email-agent-assigment
