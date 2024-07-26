# Translator app using Tune Studio and Streamlit

This repository contains the code for building a translator app that uses Tune Studio to integrate LangChain with the Mistral AI API and Streamlit for the front end. 

## Running the application

Clone this repository and navigate to the `translator-app` folder. In this folder, run the following command to create a virtual environment: 

```
python -m venv venv
```

Activate the virtual environment with the following command: 

```
source /venv/bin/activate
```

Inside the virtual environment, install the required dependencies: 

```
pip install langchain streamlit
```

Start the app by running the following command: 

```
streamlit run app.py
```

The StreamLit app will launch in your browser. You can now enter your OpenAI API key and interact with the translator app. 
