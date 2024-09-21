Doctor Appointment Chatbot Module
=================================

This application is developed to interact with a Tune Chat API, for users to book doctor appointment. The chatbot assists the user in providing necessary details for booking the appointment and confirms the details step by step.

Features
--------

*   Simulates a conversation between a user and a chatbot assistant.

*   Collects information such as patient name, contact number, appointment date, symptoms, and preferred time slot.

*   Sends a request to the tune chat API for appointment booking.

*   Parses and displays the LLM responses in real-time.


Pre-requisites
-------------

Before running this module, ensure you have:

*   **Go installed**: If you do not have Go installed, follow the official installation guide [here](https://golang.org/doc/install).

*   **API Key**: Tune Chap API.

*   **API Endpoint**: This module uses the API URL https://proxy.tune.app/chat/completions.


### 3\. Sample Conversation

When the program is executed, it will send the user converation to the tune API and parse the responses. Below is an example of a simulated conversation:

1.  **User**: Hi

2.  **Assistant**: Hello, Sid! How can I assist you today?

3.  **User**: I want to book an appointment

4.  **Assistant**: Could you provide patient name, contact information, date, time, and symptoms?

5.  **User**: Sid, mobile number 7876586442, book for September 24, 11:30 to 12:30.

6.  **Assistant**: Thank you for the details! Can you provide your symptoms?

7.  **User**: Back pain

8.  **Assistant**: Appointment has been successfully booked for September 24, 11:30 to 12:30.

