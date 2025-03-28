import imp
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import altair as alt
from PIL import Image
import base64
import tarfile
import os
import requests
from utils import *
import getUrls

# Get Latex URLs
base_url = "https://arxiv.org"
query = "machine+learning"
max_results = 50
paper_urls = getUrls.get_arxiv_paper_urls(base_url, query, max_results)
for url in paper_urls:
    print(url)
with open("arxiv_paper_urls.txt", "w") as file:
    for url in paper_urls:
        file.write(url + "\n")
print(f"Extracted {len(paper_urls)} paper URLs.")

predefined_limits = 10000

print("Crawling...")
pdf_lists = paper_urls
# cleaning the pdf lists
pdf_lists = [i.strip() for i in pdf_lists if len(i) > 0]
# TODO: limit the number of paper up to 10 since I am not sure that whether base64 support large file download
try: 
    if len(pdf_lists) > predefined_limits:
        print(f"Currently only support up to {predefined_limits} papers. Please input less than {predefined_limits} papers.")
    else:
        # parsing
        base='./download/'
        project_name = get_timestamp().replace(" ","-")
        base = os.path.join(base,project_name)
        print(base)
        time.sleep(5)
        make_dir_if_not_exist(base)
        
        N = len(pdf_lists)
        iteration = 0
        for pdf_link in pdf_lists:
            print("InfoLog-Lev1:: Processing url: ", iteration)
            iteration += 1
            title = get_name_from_arvix(pdf_link)
            file_stamp = pdf_link.split("/")[-1]
            source_link = "https://arxiv.org/e-print/"+file_stamp
            inp = os.path.join(base,'input')
            make_dir_if_not_exist(inp)
            out = os.path.join(base,'output')
            make_dir_if_not_exist(out)
            response = requests.get(source_link)
            filename = file_stamp+".tar.gz"
            filepath = os.path.join(inp,filename)
            # print(response.content)
            open(filepath, "wb").write(response.content)
            outpath = os.path.join(out,title)
            untar(filepath,outpath)


        filepath = archive_dir(out,os.path.join(base,project_name))
        b64 = ToBase64(filepath).decode()

        extract_table_from_tex(os.path.join(base,'output'))
        clean_download_dir(base)


except Exception as e:
    print("Something goes wrong. Please check the input or concat me to fix this bug. Error message: \n"+str(e))
