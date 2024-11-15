import zipfile
import os

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pickle as pkl
import py7zr

#import seaborn as sns
from tqdm import tqdm # Progress bar
import re # Regular expression operations
#from xgboost import XGBClassifier
#from sklearn.model_selection import RandomizedSearchCV
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.calibration import CalibratedClassifierCV
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.metrics import log_loss
#from sklearn.metrics import confusion_matrix
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import RandomForestClassifier

# Path to the zip file
zip_file_path = './malware-classification.zip'
# Directory to extract the contents
extract_dir = './extracted_files'

if os.path.exists(zip_file_path):
    os.makedirs(extract_dir, exist_ok=True)
    # Extract files one at a time
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        print('Extracting all the files now...')
        for file_info in zip_ref.infolist():  
            if file_info.filename in os.listdir(extract_dir):
                print('Already extracted: ', file_info.filename)
                continue
            else:
                print('Extracting {file_info.filename}...')
                zip_ref.extract(file_info, extract_dir)

    print('Extraction complete')
else:
    if os.path.exists(extract_dir):
        print('Files already extracted')
    else:
        print('Please provide the path to the zip file')
        exit()

# Extract 7z files
for root, dirs, files in os.walk(extract_dir):
    for file in files:
        if file.endswith('.7z'):
            file_path = os.path.join(root, file)
            print('file_path:', file_path)
            with py7zr.SevenZipFile(file_path, mode='r') as z:
                print(f'Extracting {file}...')
                z.extractall(path=root,)
                print(f'Extraction of {file} complete')