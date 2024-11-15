# https://www.kaggle.com/datasets/mindtrinket/malwareclassificationdatasetimages/data
# se https://www.kaggle.com/code/wahajjavedalam/notebook0921c29b4b
# https://www.kaggle.com/code/dheemanthbhat/malware-classification-with-multiprocessing
# https://www.kaggle.com/code/paulrohan2020/microsoft-malware-detection-log-loss-of-0-0070

# MS dataset description
# You are provided with a set of known malware files representing a mix of 9 different families of malware.
# Each malware file has:
#  an Id, 
# a 20 character hash value uniquely identifying the file, 
# a Class: an integer representing one of 9 family names to which the malware may belong

# For each file, 
# the raw data contains the hexadecimal representation of the file's binary content, 
# without the PE header (to ensure anonymity). 
# This binary content is stored in the form of a list of strings,

# Also provided, a metadata manifest:
# A log containin various metadata information extracted from the binary.
# such as function calls, strings, etc.

from random import shuffle
from matplotlib import pyplot as plt
import numpy as np
import os
from tqdm import tqdm
import cv2 as cv
import re

import tensorflow as tf

from sklearn.model_selection import train_test_split


# Converting malware binary to greyscale image:
# mal_binary  -> 8bit vector -> greyscale image
# for i in tqdm(range(len(data_files))):

def read_file(file_path, expected_type=None):
    file_type = re.search(r'\.\w+', file_path).group()
    if not file_type:
        print('File type not found')
        return None
    elif expected_type:
        if file_type != expected_type:
            print(f'Expected {expected_type} file type but got {file_type}')
            return None
        
    match file_type:
        case '.bytes':
            with open(file_path, 'r') as f:
                return f.read()
        case '.asm':
            with open(file_path, 'r') as f:
                return f.read()
        case '.png' | '.jpg' | '.jpeg':
            return load_img(file_path)
        case _:
            print('File type not supported')
            return None
   
def load_img(file_path):
    img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
    return img

def all_bytes_to_images(data):
    images = []
    for byte_str in data:
        img = code_to_image(byte_str)
        images.append(img)
    return images

def code_to_image(code_bytes, size=(256,256)):
    code_bytes = code_bytes.replace('?', '0')
    try:
        img= np.frombuffer(bytes.fromhex(code_bytes), dtype='uint8')#dtype='uint8'
        length=img.shape[0]
    except Exception as ValueError:
        position_num = re.search(r'\d+', str(ValueError)).group()
        print(f'character at position {position_num} is: ', code_bytes[int(position_num)])
        exit()

    #get the width
    width=int(np.ceil(np.sqrt(length)))
    height=width

    #find the length so that sqrt is whole
    new_length=np.square(width,dtype=int)

    #Not all shapes work. So pad with 0s at the end
    #calculate pad to be added
    n_pad=int(new_length-length)

    # pad the sequence length
    img_padded=np.pad(img,(0,n_pad))
    img = img_padded.reshape((width,-1))

    try:
        img = cv.resize(img, size)
        #img = (img - np.min(img)) / (np.max(img) - np.min(img))
    except Exception as e:
        print(f'Error resizing image: {e}')
        exit()

    #show the image

    return img

def get_data_from_class_dirs(data_dir,class_dict):
    data = []
    labels = []
    for i in tqdm(range(1,10),desc='Reading files'):
        class_dir = os.path.join(data_dir, class_dict[i])
        if os.path.exists(class_dir):
            files = os.listdir(class_dir)
            for j in tqdm(range(len(files)),desc=f'from {class_dict[i]}'):
                file_path = os.path.join(class_dir, files[j])
                labels.append(i)
                data.append(read_file(file_path, '.bytes'))
    
        else:
            print(f'{class_dict[i]} directory does not exist')
            continue

    return data, labels

if __name__ == '__main__':
    # Test the function
    # Read the binary file
    
    if os.path.exists('extracted_files'):
        print('Directory exists')
    else:
        print('Directory does not exist')
        exit()
    byte_train_dir = os.path.join('extracted_files', 'train','byte_files')
    byte_test_dir = os.path.join('extracted_files', 'test','byte_files')
    #asm_train_dir = os.path.join('extracted_files', 'train','asm_files')
    #asm_test_dir = os.path.join('extracted_files', 'test','asm_files')
    class_dict = {
        1:'Ramnit', 2:'Lollipop', 3:'Kelihos_ver3', 
        4:'Vundo', 5:'Simda', 6:'Tracur', 
        7:'Kelihos_ver1', 8:'Obfuscator.ACY', 9:'Gatak'}
    
    train_labels, train_byte_data = get_data_from_class_dirs(byte_train_dir, class_dict)
    print('\n Data read from class directories')
    print(f'label entries: {len(train_labels)}. byte_data entries: {len(train_byte_data)}')

    test_labels, test_byte_data = get_data_from_class_dirs(byte_test_dir, class_dict)
    print('\n Data read from class directories')
    print(f'label entries: {len(test_labels)}. byte_data entries: {len(test_byte_data)},')

    #img_train = all_bytes_to_images(train_byte_data)
    #img_test = all_bytes_to_images(test_byte_data)
    
    X_train = train_byte_data
    y_train = train_labels
    
    X_test = test_byte_data
    y_test = test_labels

    #X_train, X_test = img_train, img_test

    X_train, X_test = np.array(X_train), np.array(X_test)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2)

    X_train = np.array(X_train).astype('float32') 
    X_test = np.array(X_test).astype('float32') 
    X_val = np.array(X_val).astype('float32') 
    y_train = (np.array(y_train))
    y_test = (np.array(y_test))
    y_val = (np.array(y_val))

    model_first = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(256,256)),
        tf.keras.layers.Dense(128, activation='relu'), # 128 neurons
        tf.keras.layers.Dense(64, activation='relu'), # 64 neurons
        tf.keras.layers.Dropout(0.2), # 20% dropout idk what this is for
        tf.keras.layers.Dense(9, activation='softmax') # 9 classes. wtf is softmax?
    ])

    predictions = model_first(X_train[:1]).numpy()
    tf.nn.softmax(predictions).numpy()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model_first.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])
    
    model_first.fit(X_train, y_train, epochs=10)

    model_first.evaluate(X_test,  y_test, verbose=2)

    probability_model = tf.keras.Sequential([
    model_first,
    tf.keras.layers.Softmax()
    ])
    probability_model(X_test[:5])