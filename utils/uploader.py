import os
import time
from werkzeug.utils import secure_filename


def save_uploaded_image(file_obj, folder=None):
    """Save an uploaded image to static/uploads/ and return its URL path."""
    if not file_obj or not file_obj.filename:
        return None

    filename = secure_filename(file_obj.filename)
    if not filename:
        return None

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    unique_name = f"{int(time.time())}_{filename}"
    file_path = os.path.join(upload_dir, unique_name)
    file_obj.save(file_path)

    return f"/static/uploads/{unique_name}"


def delete_uploaded_image(image_url, folder=None):
    """Delete a locally stored image from static/uploads/."""
    if not image_url:
        return

    if image_url.startswith("/static/uploads/"):
        filename = os.path.basename(image_url)
        local_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "static", "uploads", filename
        )
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception:
                pass
