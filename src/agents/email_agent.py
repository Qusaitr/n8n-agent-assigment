import google.adk as adk
from google.adk.models import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
from src.core.config import config
from src.tools.gmail_tools import gmail_tools, search_emails, get_email_details, send_email

class EmailAgent:
    """Orchestrates the AI Email Assistant using Google ADK."""

    def __init__(self):
        self.model = LiteLlm(model=config.openai_model)
        self.system_prompt = self._get_system_prompt()
        self.agent = self._build_agent()
        self.session_service = InMemorySessionService()
        self.runner = adk.Runner(
            agent=self.agent,
            app_name="email-assistant",
            session_service=self.session_service,
        )
        self.user_id = "user_1"
        self.session_id = None

    def _get_system_prompt(self) -> str:
        return """You are a professional AI Email Assistant.

Your process follows the **ReAct (Reason + Act)** pattern:
1. **Thought**: Explain your reasoning for the next step.
2. **Action**: Select and invoke a tool.
3. **Observation**: Review the tool output and decide next steps.

**Core Workflow**:
- **Search**: Use `search_emails` to find messages based on user queries (e.g., specific subjects or keywords).
- **Read**: Use `get_email_details` to retrieve the full content (Sender, Subject, Body) of relevant emails.
- **Draft**: Generate a professional response based on the email content.
- **Human-in-the-Loop (REQUIRED)**: You MUST present the draft to the user and wait for their explicit approval before sending. 
- **Send**: Only call `send_email` if the user has explicitly confirmed the draft and given permission to send.

**Safety & Constraints**:
- Always remain professional and concise.
- Never leak sensitive information or PII.
- Handle "not found" scenarios gracefully by informing the user."""

    def _build_agent(self):
        return adk.Agent(
            name="email_assistant_agent",
            model=self.model,
            instruction=self.system_prompt,
            tools=gmail_tools  # This is already a list of functions
        )

    async def ensure_session(self):
        """Creates a session if one does not exist."""
        if self.session_id is None:
            self.session_id = f"session_{uuid.uuid4().hex[:8]}"
            await self.session_service.create_session(
                app_name="email-assistant",
                user_id=self.user_id,
                session_id=self.session_id
            )

    async def run(self, user_input: str):
        """Runs the agent asynchronously and yields content events."""
        await self.ensure_session()
        
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
        
        # session_id is guaranteed to be set after ensure_session()
        session_id = self.session_id
        assert session_id is not None
        
        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        yield part.text
