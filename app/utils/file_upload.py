import os
import uuid
from typing import Optional
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class FileUploadError(Exception):
    """Custom exception for file upload errors."""
    pass


def get_upload_folder(folder: str) -> str:
    """ Get the absolute path to the upload folder. """
    try:
        # Ensure UPLOAD_FOLDER is configured
        if 'UPLOAD_FOLDER' not in current_app.config:
            raise FileUploadError("UPLOAD_FOLDER not configured in app config")
        
        # Create the full path
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        
        # Create directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        logger.info(f"Using upload directory: {upload_dir}")
        return upload_dir
    except Exception as e:
        logger.error(f"Error getting upload folder: {str(e)}")
        raise FileUploadError(f"Failed to get upload folder: {str(e)}")


def validate_file_upload(file: FileStorage, allowed_extensions: Optional[set] = None) -> None:
    """ Validate a file upload. """
    if not file:
        raise BadRequest("No file provided")
    
    if not file.filename:
        raise BadRequest("No file selected")
    
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {
            'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'
        })
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
    if file_ext not in allowed_extensions:
        raise BadRequest(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
    
    # Check file size
    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16MB default
    file_content = file.read()
    file_size = len(file_content)
    file.seek(0)  # Reset file pointer
    
    if file_size > max_size:
        raise RequestEntityTooLarge(f"File size exceeds maximum limit of {max_size / (1024 * 1024)}MB")
    
    logger.info(f"File validated successfully: {file.filename} ({file_size} bytes)")


def save_file(file: FileStorage, folder: str) -> str:
    """ Save an uploaded file to the specified folder.  """
    try:
        # Create upload directory if it doesn't exist
        upload_dir = get_upload_folder(folder)
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Return relative path for database storage
        relative_path = os.path.join('uploads', folder, unique_filename)
        logger.info(f"File saved successfully: {relative_path}")
        return relative_path
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        raise FileUploadError(f"Failed to save file: {str(e)}")


def delete_file(file_path: str) -> None:
    """ Delete a file from the filesystem. """
    try:
        if not file_path:
            logger.warning("No file path provided for deletion")
            return
            
        # Construct full path
        full_path = os.path.join(current_app.root_path, 'static', file_path)
        
        # Check if file exists
        if not os.path.exists(full_path):
            logger.warning(f"File not found for deletion: {full_path}")
            return
            
        # Delete file
        os.remove(full_path)
        logger.info(f"File deleted successfully: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {str(e)}")
        raise FileUploadError(f"Failed to delete file: {str(e)}") 