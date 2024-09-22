import os
import tempfile
from fastapi import UploadFile

def create_temp_dir(file: UploadFile):
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path