import streamlit as st
import google.generativeai as genai
import os

api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)


def list_models():
    """Lists available Gemini models."""
    available_models = []
    for model in genai.list_models():
        print(model)
        if 'generateContent' in model.supported_generation_methods:
            print(f"Model {model.name} supports generateContent")
            available_models.append(model.name)  # Store available models
    return available_models


st.title("Gemini Chatbot")

available_models = list_models()

if not available_models:
    st.error("No available models found that support generateContent. Check your API key and region.")
else:
    selected_model_name = st.selectbox("Select a model:", available_models)
    model = genai.GenerativeModel(selected_model_name)

    # Initialize chat history in Streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Use 'chat_history' to store messages for context

    # Display existing chat messages from history
    for message in st.session_state.chat_history: # Use chat_history here
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0]) # Gemini expects 'parts' format

    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        # Append user message to chat history in the expected format
        st.session_state.chat_history.append({"role": "user", "parts": [prompt]}) # Use chat_history and 'parts'

        try:
            # Get response from Gemini, passing the entire chat history
            response = model.generate_content(st.session_state.chat_history) # Pass chat_history for context
            bot_response = response.text
        except Exception as e:
            bot_response = f"An error occurred: {e}"

        st.chat_message("assistant").markdown(bot_response)
        # Append bot response to chat history
        st.session_state.chat_history.append({"role": "model", "parts": [bot_response]}) # Use chat_history and 'parts'
