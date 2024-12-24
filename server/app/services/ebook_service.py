from app.services.openai_service import generate_content

def generate_chapters(title, target_audience):
    """
    Generates an array of chapter names based on the book title and target audience.
    """
    prompt = (
        f"Return only a array of object with chapter names for a book titled '{title}' "
        f"suitable for readers aged {target_audience}. Do not include any explanation or additional text."
        f"in this format ['chapter1 name', 'Chapter2 name']"
    )

    try:
        response = generate_content(prompt)
        # Since response is already in JSON format, it will be automatically jsonified
        return response
        
    except Exception as e:
        raise Exception(f"Error generating chapter names: {str(e)}")
    

def generateChapterContent(chapterName, story, wordCount=2000):
    """
    Generates content for a specific chapter based on the chapter name and story text.
    
    Args:
        chapterName (str): Name of the chapter to generate
        story (str): Full story text from finalbook.txt
        wordCount (int): Target word count for the chapter (default: 2000)
    
    Returns:
        str: Generated chapter content
    """
    prompt = (
        f"You are writing a chapter titled '{chapterName}' for a book. "
        f"Here is the current story context:\n\n{story}\n\n"
        "Instructions:\n"
        f"1. Generate a chapter of approximately {wordCount} words\n"
        "2. Maintain consistency with the existing story and writing style\n"
        "3. Ensure the chapter flows naturally from the previous content\n"
        "4. Include character interactions and plot development that align with the story\n"
        "5. End with a compelling hook that leads into the next chapter\n\n"
        "Return only the chapter content without any additional formatting, headers, or explanations."
    )

    try:
        response = generate_content(prompt)
        return response.strip()
        
    except Exception as e:
        raise Exception(f"Error generating chapter content: {str(e)}")