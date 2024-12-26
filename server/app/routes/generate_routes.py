from flask import Blueprint, request, jsonify
from app.services.ebook_service import generate_chapters, generateChapterContent, convert_text_to_pdf
from app.services.openai_service import save_content
import ast
import os

# Create Blueprint
generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/generate', methods=['POST'])
def generate_book():
    # Create the saved_books directory if it doesn't exist
    books_dir = "saved_books"
    if not os.path.exists(books_dir):
        os.makedirs(books_dir)
    
    # Define files without directory
    book_index_path = "bookIndex.txt"
    final_book_path = "finalbook.txt"
    final_pdf_path = "finalbook.pdf"
    
    # Create empty files if they don't exist
    if not os.path.exists(os.path.join(books_dir, book_index_path)):
        with open(os.path.join(books_dir, book_index_path), "w") as file:
            file.write("[]")  # Initialize with empty list
            
    if not os.path.exists(os.path.join(books_dir, final_book_path)):
        with open(os.path.join(books_dir, final_book_path), "w") as file:
            file.write("")
    
    data = request.json
    title = data.get('title')
    target_audience = data.get('target_audience')
    
    if not title or not target_audience:
        return jsonify({"error": "All fields are required"}), 400
        
    try:
        # Generate initial content
        content = generate_chapters(title, target_audience)
        
        # Save content without including books_dir (since save_content adds it)
        save_content(content, book_index_path)
        
        # Read chapters
        with open(os.path.join(books_dir, book_index_path), "r") as file:
            content = file.read()
            chapters = ast.literal_eval(content)
            
        # Generate chapter content
        for chapter in chapters:
            chapter = chapter.strip()
            print("Chapter ",chapter)
            if not chapter:
                continue
                
            with open(os.path.join(books_dir, final_book_path), "r") as file:
                story = file.read()
            
            chapter_content = generateChapterContent(chapter, story)
            save_content(chapter_content, final_book_path, 'a')
            
        # Convert to PDF
        print("bhai mai pahunch gaya")
        convert_text_to_pdf(os.path.join(books_dir, final_book_path), 
                          os.path.join(books_dir, final_pdf_path))
        
        return jsonify({
            "message": "Book generated successfully!", 
            "link": os.path.join(books_dir, final_book_path)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500