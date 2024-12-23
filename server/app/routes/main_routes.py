from flask import Blueprint, jsonify

# Create Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Homepage Route
    """
    return jsonify({
        "message": "Welcome to the Ebook Generator API!",
        "endpoints": {
            "/generate": "Generate an ebook",
            "/download/<filename>": "Download a generated ebook"
        }
    })

@main_bp.route('/status', methods=['GET'])
def status():
    """
    Status Route
    """
    return jsonify({"status": "API is running"})
