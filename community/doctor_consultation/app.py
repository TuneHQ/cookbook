from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import streamlit as st
from datetime import datetime

# Initialize the chat model
chat_model = ChatOpenAI(
    openai_api_key="sk-tune-Hj2Db2cpQZW0gXaTB8n8fAJp7k9XpxgzFs4",
    openai_api_base="https://proxy.tune.app/",
    model_name="Sid007/doctor-consultation"
)

def main():
    # Set the title of the app
    st.title("Hi! To book a consultation and learn about first aid for your health concern, feel free to reach out.")

    # Input fields for user data
    name = st.text_input("Patient Name", "")
    contact_number = st.text_input("Contact Number", "")
    date_of_inquiry = st.date_input("Date of Inquiry", datetime.now())
    message = st.text_area("Inquiry Message", "")

    # Preferred time slot selection
    time_slot = st.selectbox(
        "Preferred Time Slot",
        ("11:30 AM - 12:30 PM", "12:30 PM - 1:30 PM",
         "2:30 PM - 3:30 PM", "3:30 PM - 4:30 PM", "4:30 PM - 5:30 PM")
    )

    # Submit button
    if st.button("Submit"):
        if name and contact_number and message and time_slot:
            st.success(f"Thank you, {name}! Your inquiry has been submitted.")
            st.write(f"Contact Number: {contact_number}")
            st.write(f"Date of Inquiry: {date_of_inquiry}")
            st.write(f"Message: {message}")
            st.write(f"Preferred Time Slot: {time_slot}")

            # Use chat model to generate a response
            query = f"query: {message} name of the patient is {name} contact number is {contact_number} date of appointment is {date_of_inquiry} preferred time slot is {time_slot}"
            out = chat_model.predict(query)
            st.write("Response from the doctor:")
            st.write(out)
        else:
            st.error("Please fill out all fields before submitting.")

    # Optional - customize the layout of the app (if required)
    st.write("Make sure to provide correct details for us to contact you.")

if __name__ == "__main__":
    main()
