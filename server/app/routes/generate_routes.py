from flask import Blueprint, request, jsonify
from app.services.ebook_service import generate_content, save_content
from app.services.ebook_service import generate_chapters


# Create Blueprint
generate_bp = Blueprint('generate', __name__)
@generate_bp.route('/generate', methods=['POST'])
def generate_book():
    data = request.json
    title=data.get('title')
    target_audience=data.get('target_audience')
    if not title or not target_audience:
        return jsonify({"error": "All fields are required"}), 400

    try:
        content = generate_chapters(title,target_audience)
        print("generate")    
        save_content(content,"bookIndex.txt")
        print("saved")    
        return jsonify({"data": content}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
