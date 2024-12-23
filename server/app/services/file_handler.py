import os
from config import Config

def save_content(content, filename):
    file_path = os.path.join(Config.DEFAULT_OUTPUT_DIR, filename)
    with open(file_path, 'w') as file:
        file.write(content)
    return file_path
