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
    system_message = """You are a Helpful AI Email Assistant.

    RULES:
    1. **SEARCH FIRST**: Always search emails before trying to read them.
    2. **DRAFT & CONFIRM**: 
       - If asked to send an email, create a draft first.
       - Show the draft to the user.
       - ASK: "Do you want me to send this? (yes/no)"
    3. **SENDING**: Only use the 'send_message' tool if the user explicitly says "yes".
    """

    # --- MODERN 2026 IMPLEMENTATION ---
    # create_agent is the new unified API in LangChain
    app = create_agent(model=llm, tools=tools, system_prompt=system_message)
    return app

def main():
    print("=========================================")
    print("   🤖 AI Email Agent (LangGraph Native)  ")
    print("=========================================\n")
    
    check_configuration()
    
    try:
        agent_app = build_agent()
        print(f"\n✅ Agent is ready! (Model: {MODEL_NAME})\n")
        
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