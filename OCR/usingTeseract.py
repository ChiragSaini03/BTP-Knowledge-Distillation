import cv2
import pytesseract
from PIL import Image
import numpy as np
import re

def preprocess_image(image_path):
    """
    Preprocess the image for better OCR results
    """
    # Read image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(thresh, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    return img

def extract_text_from_cell(cell_image, is_math=False):
    """
    Perform OCR on a single cell and convert to LaTeX if it contains math
    """
    # Convert OpenCV image to PIL format
    pil_img = Image.fromarray(cell_image)
    
    # Configure Tesseract for better results
    custom_config = r'--oem 3 --psm 6'
    
    if is_math:
        # Use Tesseract to get the raw text first
        text = pytesseract.image_to_string(pil_img, config=custom_config)
        
        # Simple heuristic to detect math (could be enhanced)
        math_patterns = [
            r'[a-zA-Z]=[0-9]',  # Variables with assignments
            r'[0-9]+\^[0-9]+',   # Exponents
            r'\\[a-zA-Z]+',       # LaTeX commands
            r'[a-zA-Z]\([^)]+\)' # Function notation
        ]
        
        is_math = any(re.search(pattern, text) for pattern in math_patterns)
        
        if is_math:
            # Use a math OCR model if available (this is a placeholder)
            # In practice, you might want to use a specialized math OCR tool
            text = f"${text.strip()}$"  # Wrap in LaTeX math mode
            
            # Basic conversions
            text = text.replace('^', '^')    # Caret stays the same in LaTeX
            text = text.replace('*', '\\times ')  # Asterisk to times
            text = text.replace('/', '\\frac{}{}')  # Basic fraction
    else:
        text = pytesseract.image_to_string(pil_img, config=custom_config)
    
    return text.strip()

def process_table_cells(image_path, cells):
    """
    Process all cells in a table structure
    cells: List of dictionaries with x, y, width, height, and is_math flag for each cell
    """
    # Preprocess the entire image
    processed_img = preprocess_image(image_path)
    
    results = []
    
    for i, cell in enumerate(cells):
        x, y, w, h = cell['x'], cell['y'], cell['width'], cell['height']
        is_math = cell.get('is_math', False)
        
        # Extract the cell region
        cell_img = processed_img[y:y+h, x:x+w]
        
        # Perform OCR on the cell
        cell_text = extract_text_from_cell(cell_img, is_math)
        
        results.append({
            'cell_id': i,
            'coordinates': (x, y, w, h),
            'content': cell_text,
            'is_math': is_math,
            'latex_content': cell_text if is_math else None
        })
    
    return results

def generate_latex_table(results, num_columns):
    """
    Generate LaTeX table code from the OCR results
    """
    latex_code = "\\begin{tabular}{|" + "c|" * num_columns + "}\n\\hline\n"
    
    for i, result in enumerate(results):
        content = result['latex_content'] if result['is_math'] else result['content']
        latex_code += content
        
        # Add column separator or new line
        if (i + 1) % num_columns == 0:
            latex_code += " \\\\ \\hline\n"
        else:
            latex_code += " & "
    
    latex_code += "\\end{tabular}"
    return latex_code


# Example usage
if __name__ == "__main__":
    # Set Tesseract path if not in system PATH
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Example table cells (you would get these from your table detection algorithm)
    cells = [
        {'x': 0, 'y': 0, 'width': 350, 'height': 100, 'is_math': True}
    ]
    
    image_path = 'equation.png'
    
    # Process all cells
    results = process_table_cells(image_path, cells)
    
    # Generate LaTeX output
    num_columns = 2  # You should know this from your table structure
    latex_table = generate_latex_table(results, num_columns)
    
    print("OCR Results:")
    for result in results:
        print(f"Cell {result['cell_id']}: {result['content']}")
    
    print("\nLaTeX Table Code:")
    print(latex_table)

