import asyncio
import os
import sys
from src.core.config import config
from src.core.gmail_service import gmail_service_manager
from src.agents.email_agent import EmailAgent


class AgentApp:
    """Entry point for the AI Email Assistant Application."""

    def __init__(self):
        self.agent = EmailAgent()

    async def start(self):
        """Starts the interactive agent loop."""
        print("\n✉️  AI Email Assistant - Terminal Interface")
        print("------------------------------------------------")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                # In terminal environments, input() is fine for single line, 
                # but we use await in an async loop.
                user_input = input("👤 User: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                if not user_input:
                    continue

                print("🤖 Agent: ", end="", flush=True)
                
                full_response = ""
                async for chunk in self.agent.run(user_input):
                    if chunk:
                        print(chunk, end="", flush=True)
                        full_response += str(chunk)
                
                print("\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Application entry point."""
    # Ensure environment is configured
    try:
        config.validate()
        # Initialize Gmail Service early to cache credentials
        gmail_service_manager.get_service()
        
        app = AgentApp()
        asyncio.run(app.start())
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
