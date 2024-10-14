import mailbox
import json
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def message_to_dict(message):
    email_id = message['message-id'] if message['message-id'] else None
    msg_dict = {
        'id': email_id,
        'subject': message['subject'],
        'from': message['from'],
        'to': message['to'],
        'date': message['date'],
        'cc': message['cc'],
        'bcc': message['bcc'],
        'body': None
    }

    body = None
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            charset = part.get_content_charset() or 'utf-8'
            if content_type == 'text/plain':

                body = part.get_payload(decode=True).decode(charset, 'ignore')
            elif content_type == 'text/html':
                
                html_content = part.get_payload(decode=True).decode(charset, 'ignore')
                body = extract_text_from_html(html_content)
            if body:
                break  
    else:
        
        content_type = message.get_content_type()
        charset = message.get_content_charset() or 'utf-8'
        if content_type == 'text/plain':
            body = message.get_payload(decode=True).decode(charset, 'ignore')
        elif content_type == 'text/html':
            html_content = message.get_payload(decode=True).decode(charset, 'ignore')
            body = extract_text_from_html(html_content)

    msg_dict['body'] = body
    return msg_dict

def mbox_to_json(mbox_file_path, json_file_path):
    mbox = mailbox.mbox(mbox_file_path)
    messages = []

    for message in mbox:
        msg = BytesParser(policy=policy.default).parsebytes(message.as_bytes())
        msg_dict = message_to_dict(msg)
        messages.append(msg_dict)

    with open(json_file_path, 'w') as json_file:
        json.dump(messages, json_file, indent=4)

    print(f"mbox file has been converted to JSON and saved to {json_file_path}")

# Usage
mbox_file = 'source/sample.mbox'
json_file = 'data/sample.json'
mbox_to_json(mbox_file, json_file)
