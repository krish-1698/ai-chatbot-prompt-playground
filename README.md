# AI Chatbot & Prompt Playground

An interactive AI application built with Python, Streamlit, and the Google Gemini API.

## Features

- AI chatbot with conversation history
- Prompt playground for experimenting with system instructions
- Adjustable maximum output tokens
- Gemini API integration
- Clear chat functionality
- Download AI-generated responses

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- python-dotenv

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file containing your `GEMINI_API_KEY` or `OPENAI_API_KEY` .
5. Run the application:

   `streamlit run app.py`

## Security

Make sure not to commit API keys or `.env` files to GitHub.

## Future Improvements

- Model selection
- Side-by-side prompt comparison
- Saved prompt templates
- Persistent conversation history