from flask import Flask
from app.routes import main_bp, generate_bp, download_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(generate_bp)
    app.register_blueprint(download_bp)

    return app
