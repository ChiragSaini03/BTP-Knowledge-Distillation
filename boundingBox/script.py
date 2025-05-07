import cv2
import pytesseract
import pandas as pd
from openpyxl import Workbook

def image_to_excel(image_path, output_excel_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to handle varying lighting conditions
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 11, 2)
    
    # Remove noise using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Find contours to detect table structure
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area to find the table
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Draw rectangles around detected cells (optional, for visualization)
    for cnt in contours[1:10]:  # Skip the largest contour (usually the page)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Use pytesseract to extract table data
    custom_config = r'--oem 3 --psm 6'
    table_data = pytesseract.image_to_string(thresh, config=custom_config)

    # Split the data into rows and columns
    rows = table_data.split('\n')
    table = [row.split() for row in rows if row.strip()]

    # Create a DataFrame
    df = pd.DataFrame(table)

    # Save the DataFrame to an Excel file
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False)

# Example usage
image_path = 'table_image.jpg'  # Replace with your image path
output_excel_path = 'output_table.xlsx'  # Replace with your desired output path
image_to_excel(image_path, output_excel_path)
table_lines = []
