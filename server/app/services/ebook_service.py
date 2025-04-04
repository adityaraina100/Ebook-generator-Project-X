from app.services.openai_service import generate_content
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter

def generate_chapters(title, target_audience):
    prompt = (
        f"Return only a array of object with chapter names for a book titled '{title}' "
        f"suitable for readers aged {target_audience}. Do not include any explanation or additional text."
        f"in this format ['chapter1 name', 'Chapter2 name']"
        f"Keep number of chapters stricly 6."
    )

    try:
        response = generate_content(prompt)
        return response
        
    except Exception as e:
        raise Exception(f"Error generating chapter names: {str(e)}")
    

def generateChapterContent(chapterName, story, wordCount=2000):
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
    

def convert_text_to_pdf(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
        
        doc = SimpleDocTemplate(
            output_file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        style = ParagraphStyle(
            'Normal',
            fontSize=12,
            leading=16
        )
        
        story = []
        paragraphs = input_text.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                p = Paragraph(paragraph.replace('\n', '<br />'), style)
                story.append(p)
                story.append(Spacer(1, 12))
        
        doc.build(story)
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False