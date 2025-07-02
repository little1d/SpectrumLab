import base64
import re
from pathlib import Path
from typing import List, Dict, Optional, Any, Union


def encode_image_to_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to encode image to base64: {e}")


def get_image_mime_type(image_path: str) -> str:
    path = Path(image_path)
    extension = path.suffix.lower()

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
    }

    return mime_type.get(extension, "image/jpeg")


def process_images_in_question(
    question: str, image_paths: Union[str, List[str], None]
) -> str:
    if not image_paths:
        processed_question = re.sub(r"<image\d*>", "", question)
        return processed_question.strip(), []

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    image_placeholders = re.findall(r"<image\d*>", question)

    if len(image_placeholders) == 0:
        # For question without image placeholders, but image_path is not None, we need to add image to the prompt
        processed_question = f"<image>\n\n{question}"
        image_placeholders = ["<image>"]

    image_data = []
    processed_question = question

    for i, placeholder in enumerate(image_placeholders):
        if i < len(image_paths):
            image_path = image_paths[i]

            if not Path(image_path).exists():
                print(f"⚠️  Warning: Image file not found: {image_path}")
                # Remove the placeholder
                processed_question = processed_question.replace(placeholder, "", 1)
                continue

            try:
                base64_image = encode_image_to_base64(image_path)
                mime_type = get_image_mime_type(image_path)
                image_info = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}",
                    },
                }
                image_data.append(image_info)
                # Remove the placeholder
                processed_question = processed_question.replace(placeholder, "", 1)
            except Exception as e:
                print(f"⚠️  Warning: Failed to process image {image_path}: {e}")
                processed_question = processed_question.replace(placeholder, "", 1)

    return processed_question.strip(), image_data
