import os
from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()


client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key=os.getenv("HUGGINGFACE_API_KEY")
)
def generate_content(prompt):
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct", 
        messages=[
                {"role": "system", "content": "You’re a seasoned book writer with 10 years of experience in crafting compelling narratives across various genres. Your specialty lies in creating engaging stories that captivate readers and evoke emotions, ensuring that each book resonates with its intended audience.Your task is to write detailed and enticing content for the topic that is given to you.Keep in mind the importance of pacing, character development, and thematic depth as you create this outline.Also, make it as interesting and long as possible.Don't use any special characters or language other than English"},  
                {"role": "user", "content": prompt} 
            ]
            ,
        max_tokens=500
    )
    return completion.choices[0].message.content
NEW_OUTPUT_DIR = 'saved_books'

def save_content(content, filename,feature='w'):
    os.makedirs(NEW_OUTPUT_DIR, exist_ok=True) 
    file_path = os.path.join(NEW_OUTPUT_DIR, filename)
    
    with open(file_path, feature) as file:
        file.write(content)  
    
    return file_path


