import imaplib
import email
from email.header import decode_header
import datetime

def clean(text):
    # Clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def get_email_summary(email_message):
    subject = email_message["subject"]
    from_ = email_message["from"]
    date = email_message["date"]
    
    # Decode subject
    subject, encoding = decode_header(subject)[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    
    # Get the email body
    if email_message.is_multipart():
        body = ""
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()
    
    # Truncate body if it's too long
    body = body[:100] + "..." if len(body) > 100 else body
    
    return f"From: {from_}\nSubject: {subject}\nDate: {date}\nBody: {body}\n\n"

def summarize_daily_emails(email_address, password, imap_server):
    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)
    
    # Select the inbox
    imap.select("INBOX")
    
    # Get today's date
    today = datetime.date.today()
    
    # Search for emails from today
    _, message_numbers = imap.search(None, f'(SENTON {today.strftime("%d-%b-%Y")})')
    
    summary = f"Email Summary for {today}\n\n"
    
    for num in message_numbers[0].split():
        _, msg_data = imap.fetch(num, "(RFC822)")
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)
        
        summary += get_email_summary(email_message)
    
    imap.close()
    imap.logout()
    
    return summary

# Usage
email_address = "your_email@example.com"
password = "your_password"
imap_server = "imap.example.com"  # e.g., "imap.gmail.com" for Gmail

summary = summarize_daily_emails(email_address, password, imap_server)
print(summary)
