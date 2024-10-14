from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import http.client
import json
import os
from dotenv import load_dotenv
load_dotenv()

def extract_content_from_html(file_path):
    extracted_data = []

    # Open and parse the HTML file
    with open(file_path, "r") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # Loop through all <div> elements with the specified class
    for tag in soup.find_all('div', {'class': 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'}):
        text = tag.get_text(strip=True) 
        br_tag = tag.find("br")

        # Extract the text after the <br> tag
        if br_tag:
            DateToBeAppended = br_tag.find_next_sibling(string=True)
            
            try:
                # Convert the string to a datetime object
                date_object = datetime.strptime(DateToBeAppended, '%b %d, %Y, %I:%M:%S %p %Z')

                # Format the date to only display the date (YYYY-MM-DD)
                formatted_date = date_object.strftime('%Y-%m-%d')

                # Get the current date and calculate the date one month (30 days) ago
                current_date = datetime.now()
                one_month_ago = current_date - timedelta(days=60) # restricting the search till 60 days to keep the model light

                # Check if the `date_object` is within the last month
                if date_object >= one_month_ago: 
                    amountToBeAppended = extract_amount(text)  # Extract the amount from the text
                    
                    if amountToBeAppended is not None:
                         # Identify the business, person, or bank name
                        business_name = extract_business_name(text)
                        isPaid = paidOrReceived(text)

                        # Initialize the base data structure
                        data = {
                            "date": formatted_date,      
                            "paid": 0,
                            "received": 0,
                            "business_name": business_name
                        }

                        # Update the `paid` or `received` field based on the transaction type
                        if isPaid == "paid" or isPaid == "sent":
                            data["paid"] = amountToBeAppended
                        elif isPaid == "received":
                            data["received"] = amountToBeAppended

                        # Append the transaction data to the result list
                        extracted_data.append(data)
            except Exception as e:
                print(f"Error processing date: {e}")

    return extracted_data

# extract business name
def extract_business_name(text):
    # Look for "to [Business]" or "using [Bank Account]"
    to_pattern = re.search(r'to ([A-Za-z\s]+)', text)
    using_bank_pattern = re.search(r'using (Bank Account)', text)

    if to_pattern:
        return to_pattern.group(1).strip()  # Extract the business or person name
    elif using_bank_pattern:
        return "Bank Account"  # Return "Bank Account" if no business is found
    else:
        return "Unknown"  # Return Unknown if no match is found

# extract amount from string
def extract_amount(text):
    # Sample regex to extract the amount (e.g., "₹250.00")
    match = re.search(r'₹([\d,]+\.\d{2})', text)
    if match:
        return match.group(1)
    return None

# was amount paid or received
def paidOrReceived(text):
    # logic to determine the transaction type
    if "Paid" in text:
        return "paid"
    elif "Sent" in text:
        return "sent"
    elif "Received" in text:
        return "received"
    return None


def prompt_transaction_calculation(transaction_prompt, client_prompt):
    conn = http.client.HTTPSConnection("proxy.tune.app")
    payload = json.dumps({
        "temperature": 0.9,
        "messages": [
            {
                "role": "system",
                "content": transaction_prompt
            },
            {
                "role": "user",
                "content": client_prompt 
            }
        ],
        "model": "AnkurPhani/AP",
        "stream": False,
        "frequency_penalty": 0.2,
        "max_tokens": 500
    })
    headers = {
        'Authorization': os.getenv('AUTHORIZATION_KEY'),
        'Content-Type': 'application/json'
    }
    
    conn.request("POST", "/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    
    # Extract and return the desired content
    return result['choices'][0]['message']['content'] 



def cashgpt_controller(client_prompt):
    if client_prompt != "":
        # Specify the path to the HTML file
        file_path = "./My Activity.html"
        
        # Call the function and store the result
        transaction = extract_content_from_html(file_path)
        
        # Convert the transaction to a string representation
        transaction_string = str(transaction)
        # print("Transaction str", transaction)

        accountant_prompt = f"You are an experienced accountant responsible for handling your client's finances. You will be prompted by your client to analyse his financial transactions. You are provided an array of objects of your client's transactions like transaction date, paid or received amount and the name of the business the amount was paid to. \n 'date' key is the date of transaction, 'paid' is amount is paid if not zero and 'received' is amount is received if non zero. 'business_name' is the name of the business. Calculate requested calculations by your client like expenses, or received to a business or monthly or weekly expenses, Last paid amount to a business or total amount paid to a business in a month.\n\nHere is the list of all transactions\n\n{transaction_string}The output of your response needs to be formal and any amount mentioned should be in rupee (₹). Stick to the point with the answers."
        response = prompt_transaction_calculation(accountant_prompt, client_prompt)
        return response
    else:
        print("Prompt is required to continue.")

        return "no prompt to continue"