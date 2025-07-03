import base64
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


def prepare_images_for_prompt(
    image_paths: Union[str, List[str], None],
) -> List[Dict[str, Any]]:
    if not image_paths:
        return []

    # Ensure it's a list format
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    image_data = []
    for image_path in image_paths:
        if not image_path or not image_path.strip():
            continue

        path = Path(image_path)
        if not path.exists():
            print(f"⚠️  Warning: Image file not found: {image_path}")
            continue

        try:
            base64_image = encode_image_to_base64(image_path)
            mime_type = get_image_mime_type(image_path)

            image_info = {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
            }
            image_data.append(image_info)

        except Exception as e:
            print(f"⚠️  Warning: Failed to process image {image_path}: {e}")
            continue

    return image_data


def normalize_image_paths(image_paths_field: Any) -> Optional[List[str]]:
    if not image_paths_field:
        return None

    if isinstance(image_paths_field, str):
        if image_paths_field.strip() == "":
            return None
        return [image_paths_field.strip()]

    if isinstance(image_paths_field, list):
        # Filter out empty strings
        paths = [p.strip() for p in image_paths_field if p and str(p).strip()]
        return paths if paths else None

    return None
