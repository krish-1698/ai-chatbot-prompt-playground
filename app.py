import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")

api_key=os.getenv("GEMINI_API_KEY")


st.set_page_config(
    page_title="AI Chatbot & Prompt Playground",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot & Prompt Playground")


if not api_key:
    st.error("Add OPENAI_API_KEY to your .env file.")
    st.stop()


# client = OpenAI(api_key=api_key)
client = genai.Client(api_key=api_key)


MODEL = "gpt-4.1-mini"

# def generate_response(messages, max_tokens=500):
#     response = client.responses.create(
#         model=MODEL,
#         input=messages,
#         max_output_tokens=max_tokens
#     )
#     return response.output_text

def generate_response(messages, max_tokens=500):
    system_prompt = ""
    conversation = []

    for message in messages:
        if message["role"] == "developer":
            system_prompt = message["content"]
        else:
            role = (
                "model"
                if message["role"] == "assistant"
                else "user"
            )

            conversation.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ]
                )
            )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=max_tokens
        )
    )

    return response.text or "No text response generated."


tab1, tab2 = st.tabs([
    "💬 AI Chatbot",
    "🧪 Prompt Playground"
])


with tab1:
    st.header("AI Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    prompt = st.chat_input("Ask me anything...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Keep recent conversation history
                    messages = [
                        {
                            "role": "developer",
                            "content": (
                                "You are a helpful AI assistant."
                            )
                        }
                    ] + st.session_state.messages[-20:]

                    answer = generate_response(messages)
                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(f"API request failed: {e}")

with tab2:
    st.header("Prompt Playground")

    system_prompt = st.text_area(
        "System Instructions",
        value="You are a helpful AI assistant."
    )

    user_prompt = st.text_area(
        "Enter your prompt",
        placeholder="Explain machine learning.."
    )

    max_tokens = st.slider(
        "Maximum Output Tokens",
        min_value=100,
        max_value=2000,
        value=500,
        step=100
    )

    if st.button("Generate Response"):
        if not user_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating..."):
                try:
                    messages = [
                        {
                            "role": "developer",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ]

                    result = generate_response(
                        messages,
                        max_tokens=max_tokens
                    )

                    st.subheader("AI Response")
                    st.write(result)

                    st.download_button(
                        "Download Response",
                        data=result,
                        file_name="response.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"API request failed: {e}")