from PIL import Image
from pix2tex import cli as latexocr
import warnings
import time

def latex_ocr_on_segment(image_path, x, y, width, height):
    """
    Perform LaTeX OCR on a specific image segment
    Args:
        image_path: Path to input image
        x: X-coordinate of the segment start
        y: Y-coordinate of the segment start
        width: Width of the segment
        height: Height of the segment
    Returns:
        LaTeX code of the recognized content
    """
    # Open the image and crop to the specified region
    try:
        img = Image.open(image_path)
        segment = img.crop((x, y, x + width, y + height))
        segment.save("segment.png")  # Save the cropped segment for debugging
    except Exception as e:
        raise ValueError(f"Error cropping image: {str(e)}")

    # Initialize LaTeX OCR model (will auto-download weights on first run)
    model = latexocr.LatexOCR()

    # Suppress warnings about image size (common in OCR)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Convert image to RGB if needed
        if segment.mode != 'RGB':
            segment = segment.convert('RGB')
        
        # Perform LaTeX OCR
        latex_code = model(segment)

    return latex_code

if __name__ == "__main__":
    # Example usage
    print("Starting...")
    image_path = "equation.png"
    
    # Coordinates and dimensions for the segment containing math
    x = 0
    y = 0
    width = 350
    height = 100
    segments = [
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
        (0, 0, 350, 100),
    ]

    try:
        start = time.time();
        for x, y, width, height in segments:
            result = latex_ocr_on_segment(image_path, x, y, width, height)
        duration = time.time() - start
        
        print("Detected LaTeX Code:")
        print(result)
        print(f"Processed in {duration:.2f} seconds")
    except Exception as e:
        print(f"Error: {str(e)}")