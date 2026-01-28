import base64
from email.message import EmailMessage
from src.core.gmail_service import gmail_service_manager


def _get_body(payload):
    """Recursively extract the body from the message payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            body = _get_body(part)
            if body:
                return body
    if 'body' in payload and 'data' in payload['body']:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return ""


def search_emails(query: str) -> list[dict]:
    """
    Search for emails matching a subject or keyword.
    
    Args:
        query: The subject or keywords to search for.
        
    Returns:
        A list of email summaries with id and snippet.
    """
    service = gmail_service_manager.get_service()
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    summaries = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='minimal').execute()
        summaries.append({
            "id": msg['id'],
            "snippet": m.get('snippet')
        })
    return summaries


def get_email_details(message_id: str) -> dict:
    """
    Retrieve full details (Sender, Subject, Body) of a specific email.
    
    Args:
        message_id: The unique ID of the Gmail message.
        
    Returns:
        A dictionary with id, from, subject, and body.
    """
    service = gmail_service_manager.get_service()
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    
    headers = message.get('payload', {}).get('headers', [])
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'N/A')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'N/A')
    
    body = _get_body(message.get('payload', {}))
    if not body:
        body = message.get('snippet', 'No body content found.')
        
    return {
        "id": message_id,
        "from": sender,
        "subject": subject,
        "body": body
    }


def send_email(to: str, subject: str, body: str) -> dict:
    """
    Sends an email to the specified recipient.
    
    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Email body content.
        
    Returns:
        A dictionary with status and details.
    """
    service = gmail_service_manager.get_service()
    
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['Subject'] = subject
    
    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
        'raw': encoded_message
    }
    
    try:
        send_result = service.users().messages().send(userId="me", body=create_message).execute()
        return {
            "status": "success",
            "message_id": send_result.get('id'),
            "details": f"Email successfully sent to {to}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# List of tools for the agent
gmail_tools = [search_emails, get_email_details, send_email]
