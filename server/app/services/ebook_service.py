from app.services.openai_service import generate_content, save_content

def generate_chapters(title, target_audience):
    """
    Generates chapters or an index based on the topic and target audience.
    """
    prompt = (
        f"Create a table of contents for a book titled '{title}' targeted at "
        f"the audience of {target_audience} years old. Provide detailed chapter names."
    )

    try:
        chapterIndex=generate_content(prompt)
        return chapterIndex
        
    except Exception as e:
        raise Exception(f"Error generating chapters: {str(e)}")
