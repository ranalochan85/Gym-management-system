"""File handling utilities."""

import os
from datetime import datetime
from pathlib import Path


def create_upload_directory(directory: str) -> str:
    """Create upload directory if not exists."""
    upload_dir = Path(directory)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return str(upload_dir)


def generate_file_name(original_filename: str) -> str:
    """Generate unique filename."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    _, file_extension = os.path.splitext(original_filename)
    return f"{timestamp}{file_extension}"


def is_allowed_file(filename: str, allowed_extensions: list) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
