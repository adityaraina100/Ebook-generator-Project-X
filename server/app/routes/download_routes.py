from flask import Blueprint, jsonify, send_file
import os

# Create Blueprint
download_bp = Blueprint('download', __name__)

DEFAULT_OUTPUT_DIR = 'output'

@download_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Route to download a generated ebook.
    """
    file_path = os.path.join(DEFAULT_OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404
