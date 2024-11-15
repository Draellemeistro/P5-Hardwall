import zipfile
import os
import py7zr


def mkdir_and_sort_classes(data_dir='train'):
    byte_dir = os.path.join(extract_dir, data_dir, 'byte_files')
    asm_dir = os.path.join(extract_dir, data_dir, 'asm_files')
    class_dict = {
        1:'Ramnit', 2:'Lollipop', 3:'Kelihos_ver3', 
        4:'Vundo', 5:'Simda', 6:'Tracur', 
        7:'Kelihos_ver1', 8:'Obfuscator.ACY', 9:'Gatak'}
    for class_num in class_dict.keys():
        class_name = class_dict[class_num]
        #print(os.path.join(extract_dir, 'train', 'byte_files', class_name))
        print(os.path.join(extract_dir, data_dir))
        os.makedirs(os.path.join(byte_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(asm_dir, class_name), exist_ok=True)
        if os.path.exists(os.path.join(extract_dir, data_dir, 'byte_files',class_name)):
            print('Directory created successfully for: ', class_name)
        else:
            print('Failed to create directory for: ', class_name)
  
    train_labels_file = 'trainLabels.csv'
    # make symbolic links to the classes? or class folders with symbolic links to files?
    train_labels_path = os.path.join( extract_dir, train_labels_file)
    print(train_labels_path)
    csv_file = open(train_labels_path, 'r')
    csv_lines = csv_file.readlines()
    for line in csv_lines[1:]:
        line = line.split(',')
        file_name = line[0].replace('"', '').strip()
        label = line[1].strip()
        
        print('file_name:', file_name)
        #create symbolic link to the file
        if os.path.exists(os.path.join(asm_dir, file_name + '.asm')) and os.path.exists(os.path.join(byte_dir, file_name + '.bytes')):
            print('asm and byte files exist')
            sym_link_asm = os.path.join(asm_dir, class_dict[int(label)], file_name+ '.asm')
            if not os.path.exists(sym_link_asm):
                try:
                    os.symlink(os.path.abspath(os.path.join(asm_dir, file_name+'.asm')), sym_link_asm)
                except OSError as e:
                    print(f"(admin required) Failed to create symlink for {file_name}: {e}")
            
            sym_link_bytes = os.path.join(byte_dir, class_dict[int(label)], file_name+ '.bytes')
            if not os.path.exists(sym_link_bytes):
                try:
                    os.symlink(os.path.abspath(os.path.join(byte_dir, file_name+'.bytes')), sym_link_bytes)
                except OSError as e:
                    print(f"(admin required) Failed to create symlink for {file_name}: {e}")
            
            if os.path.exists(sym_link_asm) and os.path.exists(sym_link_bytes):
                print(f'Symbolic links created successfully for {file_name}')
                   
    print('class subdirs and Symbolic links created successfully')               
            


    
def sort_files(data_dir):
    byte_dest = 'byte_files'
    asm_dest = 'asm_files'
    source_dir = os.path.join(extract_dir, data_dir)
    os.makedirs(os.path.join(source_dir, byte_dest), exist_ok=True)
    os.makedirs(os.path.join(source_dir, asm_dest), exist_ok=True)
    
    data_files = os.listdir(source_dir)
    print(f'\nMoving {data_dir} files to respective subfolders...')
    for file in data_files:
        if file.endswith('.bytes'):
            os.rename(os.path.join(source_dir, file), os.path.join(source_dir, byte_dest, file))
        if file.endswith('.asm'):
            os.rename(os.path.join(source_dir, file), os.path.join(source_dir, asm_dest, file))
    
    print(f'{data_dir} files sorting complete')



if __name__ == '__main__':
    # Path to the zip file
    zip_file_path = 'MSMAL.zip'
    # Directory to extract the contents
    extract_dir = 'extracted_MS_challenge'

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
            #exit()
            

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
    mkdir_and_sort_classes()