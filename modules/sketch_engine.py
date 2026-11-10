
import cv2
import numpy as np
from PIL import Image, ImageOps


def convert_to_grayscale(image):
    """
    Convert an image into grayscale.
    """
    grayscale_image = ImageOps.grayscale(image)
    return grayscale_image




def generate_pencil_sketch(image, blur_strength=21, darkness=1.8):
    """
    Generate a pencil sketch with adjustable
    blur and pencil stroke darkness.
    """

    # Convert PIL image into NumPy array
    gray = np.array(image.convert("L"))

    # Invert grayscale image
    inverted = 255 - gray

    # Ensure blur kernel is an odd number
    if blur_strength % 2 == 0:
        blur_strength += 1

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(
        inverted,
        (blur_strength, blur_strength),
        sigmaX=0,
        sigmaY=0
    )

    # Invert blurred image
    inverted_blur = 255 - blurred

    # Apply pencil sketch algorithm
    sketch = cv2.divide(
        gray,
        inverted_blur,
        scale=256
    )

    # Increase pencil stroke darkness while preserving white areas
    sketch = 255 - (
        (255 - sketch.astype(np.float32)) * darkness
    )

    sketch = np.clip(sketch, 0, 255).astype(np.uint8)

    return Image.fromarray(sketch)


def sharpen_image(image, amount=1.0, radius=1.2):
    """
    Crisp up pencil lines with an unsharp mask.
    amount = 0 leaves the image unchanged; higher values give
    harder, more defined strokes. radius sets how wide an edge counts.
    """
    if amount <= 0:
        return image

    pixels = np.array(image).astype(np.float32)

    # Blur a copy, then push the image away from the blurred version
    blurred = cv2.GaussianBlur(pixels, (0, 0), sigmaX=radius)
    sharpened = cv2.addWeighted(pixels, 1 + amount, blurred, -amount, 0)

    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return Image.fromarray(sharpened)
