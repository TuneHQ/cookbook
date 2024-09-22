import streamlit as st
from backend import hotel_concierg

def main():
    st.title("Travel Desk Concierge")

    llm_key = st.text_input("Enter your Tune API key:", type="password")
    if not llm_key:
        st.warning("Please enter your Tune API key to continue.")
        return

    user_text = st.text_area("Please share for which city you're looking for the hotel. Please mention how many person. If need any specific requirement (e.g. pool) please mention that")
    human_input=f"Suggest hotels with {user_text}"
    if user_text:
        result = hotel_concierg(llm_key=llm_key, support_type=None, user_input=human_input)
        st.write(result)

if __name__ == "__main__":
    main()
