import io

import cv2
import numpy as np
from PIL import Image


def cartoon_image(file: bytes):
    """Convert an image to a cartoon image.
    Args:
        file (bytes): The image file.
    Returns:
        io.BytesIO: The image file in memory.
    """
    img = cv2.imdecode(np.frombuffer(file, np.uint8), -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(img, 20, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    pil_image = Image.fromarray(cartoon)
    in_mem_file = io.BytesIO()
    pil_image.save(in_mem_file, format="PNG")
    return in_mem_file
