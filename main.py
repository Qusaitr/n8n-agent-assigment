import os
import sys
from dotenv import load_dotenv

# Google Auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# LangChain & LangGraph
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import build_resource_service
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
SCOPES = os.getenv('GOOGLE_SCOPES', 'https://mail.google.com/').split(',')
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
TOKEN_FILE = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')
MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-4o')

def check_configuration():
    """Validates configuration presence."""
    errors = []
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("❌ OPENAI_API_KEY not found in .env file.")
    if not os.path.exists(CREDENTIALS_FILE):
        errors.append(f"❌ '{CREDENTIALS_FILE}' not found.")
    
    if errors:
        print("\n⚠️  CONFIGURATION ERROR")
        for err in errors:
            print(err)
        sys.exit(1)

def get_gmail_credentials():
    """Handles OAuth2 authentication."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for login...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def build_agent():
    """Initializes the Modern LangGraph Agent."""
    print("🔐 Authenticating with Gmail...")
    creds = get_gmail_credentials()
    
    # Setup Tools
    api_resource = build_resource_service(credentials=creds)  # type: ignore
    toolkit = GmailToolkit(api_resource=api_resource)
    tools = toolkit.get_tools()
    
    # Setup LLM
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

    # System Instructions
    system_message = """You are an AI email assistant that helps users respond to emails. Your workflow:

1. **Get Email Subject/Keywords First**: If the user hasn't provided specific email subject keywords, ask: "Please provide the email subject (or keywords) to search for." Don't proceed until you have clear search terms.
2. **Search for Emails**: Use the Gmail Search Tool to find emails matching the subject/keywords provided
3. **Retrieve Full Email**: Once you find matching emails, use the Gmail Get Email Tool to retrieve the full email content (from, subject, body)
4. **Display Email Details**: Show the email details clearly to the user (From, Subject, Body)
5. **Generate Reply**: Create a thoughtful, professional reply based on the email content and context
6. **Show Draft & Request Confirmation**: Present the suggested reply to the user and ask: "Would you like me to send this reply? You can: (1) Approve and send, (2) Request modifications, or (3) Reject"
7. **Handle User Decision**:
   - If user APPROVES (says "yes", "send it", "looks good", "approve", etc.), use the Gmail Send Tool to send the reply
   - If user wants MODIFICATIONS (says "change this", "make it shorter", etc.), adjust the reply and ask for confirmation again
   - If user REJECTS (says "no", "don't send", "cancel"), acknowledge and do not send
8. **Confirm Success**: After sending, confirm the email was sent successfully

**Available Tools:**
- **Gmail Search Tool**: Search for emails by subject or keywords. Returns a list of matching email IDs and basic information.
- **Gmail Get Email Tool**: Retrieve the full content of a specific email by its message ID. Returns from, subject, body, and other details.
- **Gmail Send Tool**: Send an email reply to a recipient. Requires recipient email, subject, and message body. **ONLY use this after getting explicit user approval.**

**Critical Rules:**
- If no subject/keywords provided in the initial message, ASK for them explicitly before searching
- ALWAYS search before reading emails (to get valid message IDs)
- NEVER send emails without explicit user approval ("yes", "send", "approve")
- If user says "modify" or "change", update the draft and ask again
- If user says "no" or "reject", do not send and acknowledge their decision
- Always be helpful, professional, and respectful of user consent

Remember: User safety and consent are paramount."""

    # --- MODERN 2026 IMPLEMENTATION ---
    # create_agent is the new unified API in LangChain
    app = create_agent(model=llm, tools=tools, system_prompt=system_message)
    return app

def main():
    """Main execution loop with conversational interface."""
    print("=========================================")
    print("   🤖 AI Email Agent (LangGraph Native)  ")
    print("=========================================\n")
    
    check_configuration()
    
    try:
        agent_app = build_agent()
        print(f"\n✅ Agent is ready! (Model: {MODEL_NAME})\n")
        print("💡 How to use: Provide an email subject or keywords to search for.")
        print("   Example: 'Find emails about project proposal'\n")
        
        # We maintain a list of messages for context
        chat_history = [] 
        
        while True:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue

            print("🤖 Agent is thinking...", end="\r")

            # Prepare the input for the graph
            current_messages = chat_history + [HumanMessage(content=user_input)]
            
            # Execute
            response = agent_app.invoke({"messages": current_messages})
            
            # Extract the last message (AI's reply)
            last_message = response["messages"][-1]
            print(f"\n🤖 Agent: {last_message.content}\n")
            
            # Update history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(last_message)

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()