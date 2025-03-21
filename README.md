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


```
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
