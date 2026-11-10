
from PIL import Image, ImageOps
from io import BytesIO


def validate_image(uploaded_file):
    """
    Validate uploaded image format and dimensions.
    """

    if uploaded_file is None:
        return False, "No image uploaded."

    try:
        image = Image.open(BytesIO(uploaded_file.getvalue()))

        # Check supported formats
        if image.format not in ["JPEG", "PNG"]:
            return False, "Only JPG, JPEG and PNG images are supported."

        # Check image dimensions
        width, height = image.size

        if width < 100 or height < 100:
            return False, "Image dimensions must be at least 100 x 100 pixels."

        # Respect phone camera orientation (EXIF) while keeping the format label
        original_format = image.format
        image = ImageOps.exif_transpose(image)
        image.format = original_format

        return True, image

    except Exception:
        return False, "Invalid or corrupted image file."
