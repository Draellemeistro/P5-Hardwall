import zipfile
import os
import py7zr
from tqdm import tqdm # Progress bar

def sort_files(data_dir):
    byte_dest = 'byte_files'
    asm_dest = 'asm_files'
    source_dir = os.path.join(extract_dir, data_dir)
    os.makedirs(os.path.join(source_dir, byte_dest), exist_ok=True)
    os.makedirs(os.path.join(source_dir, asm_dest), exist_ok=True)
    
    data_files = os.listdir(source_dir)
    print(f'\nMoving {data_dir} files to respective subfolders...')
    for i in tqdm(range(len(data_files))):
        file = data_files[i]
        if file.endswith('.bytes'):
            os.rename(os.path.join(source_dir, file), os.path.join(source_dir, byte_dest, file))
        if file.endswith('.asm'):
            os.rename(os.path.join(source_dir, file), os.path.join(source_dir, asm_dest, file))
    
    print(f'{data_dir} files sorting complete')

if __name__ == '__main__':
    # Path to the zip file
    zip_file_path = './malware-classification.zip'
    # Directory to extract the contents
    extract_dir = './MS_malware_extracted'

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
                    print(f'Extracting {file_info.filename}...')
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
            if file == 'dataSample.7z':
                continue
            if file.endswith('.7z') and not os.path.exists(os.path.join(root, file.split('.')[0])):
                print(os.path.join(root, file.split('.')[0]))
                file_path = os.path.join(root, file)
                print('file_path:', file_path)
                with py7zr.SevenZipFile(file_path, mode='r') as z:
                    print(f'Extracting {file}...')
                    z.extractall(path=root,)
                    print(f'Extraction of {file} complete')


    sort_files('train')
    sort_files('test')

    print('\n###############################################################\n',
        'All files extracted and sorted successfully')