## BTP-Knowledge-Distillation

### Initial Idea
- Table image to latex
- Many models available
- struggle with accuracy of models

### Enhanced Idea
- Table image to excel
    -   Extract the table structure - more accurate the structure, more accurate the latex
    -   Extract the cell data and put on the excel table using OCR
- Excel to latex conversion using standard script

### Table to Excel?
- 

### Excel to Latex
- col, row, multi-row, multi-col, 
- latex tags to be used -> 
- colour and styling should not be considered as table color and other things not to be considered


### Setup
For running the project:
- Create a virtual python environment using pip
- Install the dependencies
    - pip install requirements.txt
- run the base file


### Another approach
- bounding boxes in table and then extracting the content from each bounding box (can be done parallely), then creating an algorithm to convert the bounding box info and text info for bounding box <--> excel table using code.


- ```
    Bounding box info schema:-
    {
        no: int,
        coord: {
            x: int,
            y: int
        },
        width: int,
        height: int,
        content: string(extracted through OCR)
    }
    ```

-  Do we need an initial model to convert a table with incomplete border or non bordered table to bordered table. 


1 Lakhs - 2 lakhs images -> to train and do all the model analytics.


### Code Flow
- /arxivToLatex -> Data preperation -- To fetch all the arxiv research papers and filter out tables latex code from it
- /boundingbox -> detect the bounding box of each cell with half filled bound box json.
- /OCR -> extract the contect of each cell in each bounding box - can be done parallely for each cell. -> fetching each cell data reduces our OCR complexity and makes the process faster
- /cellJsonToExcel -> convert the fetched json to excel using algorithm
- /excelToLatex -> convert the excel to latex

Note: The third and fourth step can be combined, if we directly convert the cellJson to latex


- Works with table images with all borders in table.

