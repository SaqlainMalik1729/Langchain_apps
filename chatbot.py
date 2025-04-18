from langchain_openai import ChatOpenAI
import streamlit as st
#from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set. Please configure it in the environment.")
    st.stop()
    
model = ChatOpenAI(api_key=OPENAI_API_KEY)

# Custom CSS for ChatGPT-like UI with mobile compatibility
st.markdown("""
    <style>
    /* General app styling */
    .stApp {
        background-color: #f0f2f6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 10px;
        box-sizing: border-box;
    }
    
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #343541;
            color: #ececf1;
        }
        .heading {
            color: #ececf1;
        }
        div[data-testid="stChatMessage"][data-user="false"] {
            background-color: #444654;
        }
        div[data-testid="stChatInput"] {
            background-color: #40414f;
        }
        div[data-testid="stChatInput"] input {
            color: #ececf1;
        }
    }
    
    /* Heading styling */
    .heading {
        font-size: 24px;
        font-weight: 600;
        color: #575348;
        text-align: center;
        margin: 15px 0;
    }
    
    /* Initial icon container */
    .icon-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40vh;
    }
    .icon {
        font-size: 60px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        margin: 6px 0;
        padding: 10px 12px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.4;
    }
    
    /* User message */
    div[data-testid="stChatMessage"][data-user="true"] {
        background-color: #d1e8d5;
        color: #0a3c17;
        margin-left: 10%;
        text-align: left;
    }
    
    /* Assistant message */
    div[data-testid="stChatMessage"][data-user="false"] {
        background-color: #ffffff;
        color: #333;
        margin-right: 10%;
        text-align: left;
    }
    
    /* Chat input styling */
    div[data-testid="stChatInput"] {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 8px;
        padding: 8px;
        position: fixed;
        bottom: 10px;
        width: calc(100% - 40px);
        max-width: 760px;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
        box-sizing: border-box;
    }
    div[data-testid="stChatInput"] input {
        color: #333;
        background-color: transparent;
        font-size: 14px;
    }
    
    /* Clear chat button */
    .stButton > button {
        background-color: transparent;
        color: #666;
        border: 1px solid #dcdcdc;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 12px;
        position: fixed;
        top: 10px;
        right: 10px;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #f5f5f5;
        color: #333;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: #10a37f;
    }
    
    /* Hide Streamlit branding */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main > div {
        padding: 0;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 600px) {
        .stApp {
            padding: 5px;
        }
        .heading {
            font-size: 20px;
            margin: 10px 0;
        }
        .icon-container {
            height: 30vh;
        }
        .icon {
            font-size: 50px;
        }
        .stChatMessage {
            margin: 4px 0;
            padding: 8px 10px;
            font-size: 13px;
        }
        div[data-testid="stChatMessage"][data-user="true"] {
            margin-left: 5%;
        }
        div[data-testid="stChatMessage"][data-user="false"] {
            margin-right: 5%;
        }
        div[data-testid="stChatInput"] {
            width: calc(100% - 20px);
            bottom: 5px;
            border-radius: 6px;
            padding: 6px;
        }
        div[data-testid="stChatInput"] input {
            font-size: 13px;
        }
        .stButton > button {
            padding: 4px 8px;
            font-size: 11px;
            top: 5px;
            right: 5px;
        }
        * Hide Streamlit branding and footer */
    footer, [data-testid="stFooter"], .streamlit-footer, .viewerBadge_container__1QSob {
        display: none !important;
    }
    }
    </style>
""", unsafe_allow_html=True)

# Heading
st.markdown('<div class="heading">Chatbot</div>', unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful AI assistant")
    ]

# Function to clear chat history
def clear_chat():
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful AI assistant")
    ]

# Display clear chat button
st.button("New Chat", on_click=clear_chat)

# Check if conversation has started
has_conversation = any(isinstance(msg, HumanMessage) for msg in st.session_state.chat_history)

# Display initial icon if no conversation
if not has_conversation:
    st.markdown(
        '<div class="icon-container"><span class="icon">🤖</span></div>',
        unsafe_allow_html=True
    )

# Display chat history only if conversation has started
if has_conversation:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get AI response
    with st.spinner(""):
        try:
            result = model.invoke(st.session_state.chat_history)
            ai_response = result.content
        except Exception as e:
            ai_response = f"Error: {str(e)}"
    
    # Append and display AI response
    st.session_state.chat_history.append(AIMessage(content=ai_response))
    with st.chat_message("assistant"):
        st.write(ai_response)
