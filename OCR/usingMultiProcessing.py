from PIL import Image
from pix2tex import cli as latexocr
import warnings
import multiprocessing
import time

# Global variable for worker processes
_model = None

def init_worker():
    """Initialize worker process with LaTeX OCR model"""
    global _model
    _model = latexocr.LatexOCR()
    warnings.filterwarnings("ignore")

def process_segment(args):
    """Process a single image segment with LaTeX OCR"""
    image_path, x, y, width, height = args
    try:
        # Open and crop image segment
        with Image.open(image_path) as img:
            segment = img.crop((x, y, x + width, y + height))
            # if segment.mode != 'RGB':
            #     segment = segment.convert('RGB')
            
            # Perform OCR with the pre-initialized model
            latex_code = _model(segment)
            
            return {
                'coordinates': (x, y, width, height),
                'latex': latex_code,
                'error': None
            }
    except Exception as e:
        return {
            'coordinates': (x, y, width, height),
            'latex': None,
            'error': str(e)
        }

def parallel_latex_ocr(image_path, segments, num_processes=None):
    """
    Process multiple image segments in parallel
    Args:
        image_path: Path to the input image
        segments: List of tuples (x, y, width, height)
        num_processes: Number of parallel processes (default: CPU count)
    Returns:
        List of results with LaTeX code and coordinates
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    print(f"Number of processing units: {num_processes}")

    # Prepare arguments for each segment
    tasks = [(image_path, x, y, w, h) for (x, y, w, h) in segments]

    with multiprocessing.Pool(
        processes=num_processes,
        initializer=init_worker
    ) as pool:
        results = pool.map(process_segment, tasks)

    return results

if __name__ == "__main__":
    # Required for Windows support
    multiprocessing.freeze_support()

    # Example usage
    image_path = "equation.png"
    
    # Define multiple segments to process (x, y, width, height)
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

    start = time.time()
    # Process segments in parallel
    results = parallel_latex_ocr(image_path, segments)
    duration = time.time() - start


    # Print results
    for i, result in enumerate(results):
        print(f"\nSegment {i+1} ({result['coordinates']}):")
        if result['error']:
            print(f"Error: {result['error']}")
        else:
            print(f"LaTeX: {result['latex']}")
    print(f"Total time taken to process segments: {duration:.2f} seconds")

