import sys
import os

# Get the absolute path of the Project folder (root directory)
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the Project folder to sys.path
if project_dir not in sys.path:
    sys.path.append(project_dir)

import utils

def extractTableFromTexSpec():
    folder = "./download/20250323164907/output/"

    utils.extract_table_from_tex(folder)



if __name__ == "__main__":
    extractTableFromTexSpec()
