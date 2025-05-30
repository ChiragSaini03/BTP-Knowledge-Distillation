import tarfile
import os
import requests
import datetime
import pandas as pd
import shutil
from bs4 import  BeautifulSoup
from tqdm import tqdm
import base64
import shutil
from pathlib import Path

def ToBase64(file):
    with open(file, 'rb') as fileObj:
        data = fileObj.read()
    base64_data = base64.b64encode(data)
    return base64_data

def archive_dir(dir_name,output_filename,format="zip"):
    shutil.make_archive(output_filename, format, dir_name)
    return output_filename+".zip"

def make_dir_if_not_exist(folder):
  if not os.path.exists(folder):
    os.makedirs(folder)

def untar(fname, dirs):
    try:
        t = tarfile.open(fname)
        t.extractall(path = dirs)
        return True
    except Exception as e:
        print(e)
        return False

def get_timestamp():
    ts = pd.to_datetime(str(datetime.datetime.now()))
    d = ts.strftime('%Y%m%d%H%M%S')
    return d

def get_name_from_arvix(url):
    res = BeautifulSoup(requests.get(url).content, 'lxml').find("h1",attrs={"class":"title mathjax"})
    if res is None:
        return ''
    title = res.text[6:].replace(" ","-")
    return title

def extract_table_from_tex(outFolder):
    # Read tex code from all files and then fetch the text between \begin{table} and \end{table} and write it in a seperate file.
    # here folder is the output folder
    try:
        folders = [item.name for item in Path(outFolder).iterdir() if item.is_dir()]

        files = [f"{outFolder}/{folder}/{f}" for folder in folders for f in os.listdir(f"{outFolder}/{folder}/") if f.endswith('.tex')]

        for file in files:
            try:
                with open(file, 'r', encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                table_lines = []
                inside_table = False

                for line in lines:
                    if r"\begin{table" in line:
                        table_lines.append(line)
                        inside_table = True
                    elif r"\end{table" in line:
                        if len(table_lines) > 0:
                            table_lines.append(line)
                            current_dir = os.getcwd()

                            metadata_file = os.path.join(current_dir, "metadata.txt")
                            with open(metadata_file, 'r') as cf:
                                cnt = cf.read()
                                if (cnt == ''):
                                    cnt = 0
                                else:
                                    cnt = int(cnt)
                            
                            with open(metadata_file, 'w') as cf:
                                cnt += 1
                                cf.write(str(cnt))
                            table_file = current_dir + r"\data\table_" + str(cnt) + ".txt"
                            print(table_file)
                            with open(table_file, 'w') as tf:
                                tf.writelines(table_lines)
                        
                        table_lines = []
                        inside_table = False
                        print("InfoLog-Lev3:: Table found and written to file...")
                    elif (inside_table):
                        table_lines.append(line)
            except Exception as e:
                print("ErrorLog-Lev3:: ", e)
    except Exception as e:
        print("ErrorLog-Lev3:: ", e)

def clean_download_dir(folder):
    print(folder)
    if (os.path.exists(folder)):
        shutil.rmtree(folder, ignore_errors=False)

def download_source(pdf_lists=None,output_base=None,project_name=None,fetch_title=True, return_source=False):
    base=output_base
    project_name = project_name + get_timestamp()
    base = os.path.join(base,project_name)
    make_dir_if_not_exist(base)
    
    for pdf_link in tqdm(pdf_lists):
        file_stamp = pdf_link.split("/")[-1]
        if fetch_title:
            title = get_name_from_arvix(pdf_link)
            if len(title )== 0:
                continue
        else:
            import numpy as np
            title = file_stamp
        source_link = "https://arxiv.org/e-print/"+file_stamp
        inp = os.path.join(base,'input')
        make_dir_if_not_exist(inp)
        out = os.path.join(base,'output')
        make_dir_if_not_exist(out)
        if return_source:
            print(source_link)
            continue
        response = requests.get(source_link)
        filename = file_stamp+".tar.gz"
        filepath = os.path.join(inp,filename)
        open(filepath, "wb").write(response.content)
        outpath = os.path.join(out,title)
        untar(filepath,outpath)
    archive_dir(out,os.path.join(base,project_name))

if __name__ == '__main__':
    s = get_timestamp()
    print(s)

