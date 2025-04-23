import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Debug print
print("DEBUG: ", os.getenv("GROQ_API_KEY"))

groq_api_key = os.getenv("GROQ_API_KEY")

# DEBUG: Check if it loaded
if groq_api_key is None:
    st.error("API key not found! Check your .env file.")
    st.stop()

# Initialize client
client = Groq(api_key=groq_api_key)

st.sidebar.title("Personalization")
prompt = st.sidebar.title("System Prompt: ")
model = st.sidebar.selectbox(
    "Choose a Model", ["Llama3-8b-8192","Llama3-70b-8192"]
    )

#Groq Client
client = Groq(api_key=groq_api_key)

#streamlit Interface
st.title(" 💭 Chat with Groq's LLM")

#initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Enter your prompt: ", "")

if st.button("Submit"):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user",
             "content" : user_input
             },
        ],
        model=model, 
    )
    # Store the prompt and response in history
    response = chat_completion.choices[0].message.content
    st.session_state.history.append({"prompt": user_input, "response": response})

    #Display the response
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

    #Display history 
    st.sidebar.title("History")
    for i, entry in enumerate(st.session_state.history):
        if st.sidebar.button(f'Prompt {i+1}:{entry["prompt"]}'):
            st.markdown(f'<div class="response-box">{entry["response"]}</div>', unsafe_allow_html=True)
            
  