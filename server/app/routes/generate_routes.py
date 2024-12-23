from flask import Blueprint, request, jsonify
from app.services.ebook_service import  save_content, generate_chapters, generateChapterContent
import json
import ast
# Create Blueprint
generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/generate', methods=['POST'])
def generate_book():
    data = request.json
    title = data.get('title')
    target_audience = data.get('target_audience')
    
    if not title or not target_audience:
        return jsonify({"error": "All fields are required"}), 400

    try:
        content = generate_chapters(title, target_audience)
        save_content(content, "bookIndex.txt")

        with open("saved_books/bookIndex.txt", "r") as file:
            content = file.read()
            chapters = ast.literal_eval(content)

        with open("saved_books/finalbook.txt", "r") as file:
                story = file.read()
        for chapter in chapters:
            chapter = chapter.strip() 
            if not chapter:  # Skip empty lines
                continue
            
            
            chapter_content = generateChapterContent(chapter,story )
            save_content(chapter_content, chapter + ".txt")
        
        return jsonify({"message": "Book generated successfully!", "link": "/path/to/finalbook.txt"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500