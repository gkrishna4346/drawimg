
from PIL import Image


def remove_background(image):
    """
    Remove the background from an image
    and replace transparency with white.
    """
    # Imported lazily: rembg loads a large model, so the app starts
    # quickly and only pays that cost when the feature is used.
    from rembg import remove

    # Ensure the input image supports transparency
    image = image.convert("RGBA")

    # Remove background using rembg
    foreground = remove(image)

    # Create a white background
    white_background = Image.new(
        "RGBA",
        foreground.size,
        (255, 255, 255, 255)
    )

    # Combine foreground with white background
    final_image = Image.alpha_composite(
        white_background,
        foreground
    )

    # Return RGB image
    return final_image.convert("RGB")
