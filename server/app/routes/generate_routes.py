import time
from flask import Blueprint, request, jsonify
from app.services.ebook_service import generate_chapters, generateChapterContent, convert_text_to_pdf
from app.services.openai_service import save_content
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
import ast
import os

generate_bp = Blueprint('generate', __name__)
client = Client()
AppEndpoint = os.getenv("APP_EP")
BucketID = os.getenv("APP_BUCKETID")
ProjectID = os.getenv("APP_PID")
client.set_endpoint(AppEndpoint) 
client.set_project(ProjectID) 
client.set_key(os.getenv("APP_KEY"))        

storage = Storage(client)

@generate_bp.route('/generate', methods=['POST'])
def generate_book():
    
    data = request.json
    title = data.get('title')
    target_audience = data.get('target_audience')

    books_dir = "saved_books"
    book_index_path = "bookIndex.txt"
    final_book_path = "finalbook.txt" 
    truncated_title = title.replace(' ', '_')[:10]
    final_pdf_path = f"{truncated_title}.pdf"
    if not os.path.exists(books_dir):
        os.makedirs(books_dir)
    if not os.path.exists(os.path.join(books_dir, book_index_path)):
        with open(os.path.join(books_dir, book_index_path), "w") as file:
            file.write("[]") 
            
    if not os.path.exists(os.path.join(books_dir, final_book_path)):
        with open(os.path.join(books_dir, final_book_path), "w") as file:
            file.write("")  
    
    
    if not title or not target_audience:
        return jsonify({"error": "All fields are required"}), 400
        
    try:
        content = generate_chapters(title, target_audience)
        save_content(content, book_index_path)
        with open(os.path.join(books_dir, book_index_path), "r") as file:
            content = file.read()
            chapters = ast.literal_eval(content)
        for chapter in chapters:
            chapter = chapter.strip()
            print("Chapter ",chapter)
            if not chapter:
                continue      
            with open(os.path.join(books_dir, final_book_path), "r") as file:
                story = file.read()
            chapter_content = generateChapterContent(chapter, story)
            save_content(chapter_content, final_book_path, 'a')
        pdf_path = os.path.join(books_dir, final_pdf_path)
        convert_text_to_pdf(os.path.join(books_dir, final_book_path), pdf_path)
        try:
                pdf_path = os.path.join(books_dir, final_pdf_path)
                file_id = f'book_{title.replace(" ", "_")}_{int(time.time())}'
                print("File ID: ", file_id)
                result = storage.create_file(
                    bucket_id=BucketID,
                    file_id=file_id,
                    file=InputFile.from_path(pdf_path)
                )
                file_id = result['$id']
                file_url = f'{AppEndpoint}/storage/buckets/{BucketID}/files/{file_id}/view?project={ProjectID}'
                os.remove(pdf_path)
                os.remove(os.path.join(books_dir, final_book_path))
                os.remove(os.path.join(books_dir, book_index_path))
                os.rmdir(books_dir)
           
                return jsonify({
                    "message": "Book generated and uploaded successfully!", 
                    "file_id": file_id,
                    "file_url": file_url
                }), 200
        except Exception as upload_error:
            return jsonify({"error": f"Failed to upload PDF: {str(upload_error)}"}), 500    
    except Exception as e:
        return jsonify({"error": str(e)}), 500