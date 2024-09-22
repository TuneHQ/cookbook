# Play tic tac toe

This repository contains the code for building a tic tac toe app that uses Tune Studio to integrate LangChain with the Tune studio API and Streamlit for the front end. 

## Running the application

Clone this repository and navigate to the `translator-app` folder. In this folder, run the following command to create a virtual environment: 

```sh
python -m venv venv
```

Activate the virtual environment with the following command: 

```sh
source venv/bin/activate
```

Inside the virtual environment, install the required dependencies: 

```sh
pip install langchain langchain-openai streamlit
```

Start the app by running the following command: 

```sh
streamlit run app.py
```

The StreamLit app will launch in your browser. You can now enter your OpenAI API key and interact with the translator app. 


## How to play

1. Enter the prompt `Lets play tic tac toe`
2. You will get a response of a 3*3 grid
3. use the number from 1-9 for position inputs.
4. What are you waiting for? Lets get started!!

![image](https://github.com/user-attachments/assets/86b94be9-2cdc-4d0b-b4d0-aab9ff124435)
