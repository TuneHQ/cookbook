# Ready for JOKE

This repository contains the code for building a AI comedian  app that uses Tune Studio to integrate LangChain with the Tune studio API and Streamlit for the front end. 


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
