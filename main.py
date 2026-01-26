import requests
import uuid
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
# IMPORTANT FOR EVALUATOR:
# 1. Import the provided 'agent_workflow.json' into your local n8n instance.
# 2. Configure your Gmail and OpenAI credentials in the nodes.
# 3. Activate the workflow.
# 4. Ensure the Chat Trigger node Authentication is set to 'None'.
# 5. If your local URL is different, update it below:
# Load environment variables from .env file
load_dotenv()

# Get webhook URL from environment variable, fallback to default
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/email-agent/chat")

def chat_with_agent():
    # Generate a unique session ID for conversation memory
    session_id = str(uuid.uuid4())

    print("--- AI Email Response Agent ---")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            # Prepare payload for n8n Chat Trigger
            payload = {
                "chatInput": user_input,
                "sessionId": session_id
            }

            print("Agent is thinking...", end="\r")

            # Send request to n8n backend
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
            response.raise_for_status()
            
            # Parse response from n8n
            data = response.json()
            # The Chat Trigger returns the answer in the 'output' field
            agent_reply = data.get('output', "No text response received from agent.")

            # Print the reply
            # Clear the "thinking" line
            print(f"Agent: {agent_reply}\n")

        except requests.exceptions.ConnectionError:
            print(f"\n[Error] Could not connect to n8n at {N8N_WEBHOOK_URL}.")
            print("Please ensure your n8n workflow is Active and running locally.\n")
        except Exception as e:
            print(f"\n[Error] An issue occurred: {e}\n")

if __name__ == "__main__":
    chat_with_agent()
