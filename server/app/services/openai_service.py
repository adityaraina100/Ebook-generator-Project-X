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
            {"role": "system", "content": "You are a helpful assistant."},  # Initial system message
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

# Example usage:
if __name__ == "__main__":
    prompt = "Tell me about the benefits of learning Python."
    generated_text = generate_content(prompt)
    print("Generated Content:\n", generated_text)
    save_path = save_content(generated_text, "python_benefits.txt")
    print(f"Content saved to {save_path}")
