import os
from dotenv import load_dotenv # type: ignore
import openai # type: ignore

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv("OPEN_AI_KEY")

def generate_content(prompt):
    """
    Generate content using OpenAI GPT model.
    """

    # Set the OpenAI API key before making a request
    openai.api_key = openai_api_key

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": '''You’re a seasoned book writer with 10 years of experience in crafting compelling narratives across various genres. Your specialty lies in creating engaging stories that captivate readers and evoke emotions, ensuring that each book resonates with its intended audience.
            Your task is to write detailed and enticing content for the topic that is given to you.Keep in mind the importance of
              pacing, character development, and thematic depth as you create this outline.Also, make it as interesting and long ass possible.'''},  # Initial system message
            {"role": "user", "content": prompt}  # User prompt
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

NEW_OUTPUT_DIR = 'saved_books'

def save_content(content, filename):
    os.makedirs(NEW_OUTPUT_DIR, exist_ok=True)  # Create directory if it doesn't exist
    file_path = os.path.join(NEW_OUTPUT_DIR, filename)
    
    with open(file_path, 'w') as file:
        file.write(content)  # Save the content to a file
    
    return file_path
