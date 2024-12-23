import os

class Config:
    OPENAI_API_KEY = 'your-api-key'  # Replace with your OpenAI API key
    DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
