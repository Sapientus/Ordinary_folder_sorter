import sys
import os
from pathlib import Path
#from glob import glob
import shutil

images = []            #hey buddy, here we create empty lists to add files` names here in the future
video = []
documents = []
audio = []
archives =  []
known_extensions = set()
unknown_extensions = set()
all_adresses = []
all_folders = ['Images', 'Video', 'Documents', 'Audio', 'Archives']

extensions_we_sort = {     #this is our dictionary, we`ll use it to find all extensions we need
    'jpeg' : images, 
    'png' : images,
    'jpg' : images,
    'svg' : images,
    'avi' : video,
    'mp4' : video,
    'mov' : video,
    'mkv' : video,
    'doc' : documents,
    'docx' : documents,
    'txt' : documents,
    'pdf' : documents,
    'xlsx' : documents,
    'pptx' : documents,
    'mp3' : audio, 
    'ogg' : audio, 
    'wav' : audio,
    'amr' : audio,
    'zip' : archives,
    'gz' : archives,
    'tar' : archives
}

def sorting(folder_path):     #here we're sorting our files into lists
    for i in folder_path.iterdir():
        if i.is_file():
            for key in extensions_we_sort.keys():
                if str(i.suffix.replace('.', '')) in extensions_we_sort.keys():
                    all_adresses.append(i)
                    if str(i.suffix.replace('.', '')) == key:
                        extensions_we_sort[key].append(i.name)
                        known_extensions.add(str(i.suffix.replace('.', '')))
                else:
                    unknown_extensions.add(str(i.suffix.replace('.', '')))
        else:
            sorting(i)

KYRILLIC_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюяыъэё'   #ah, of course, we create dictionary to transliterate names
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja", "y", "i", "yo")

TRANS = {}
for key, value in zip(KYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(file_name):   #don`t worry, buddy, this will change scary files` names into readable ones
    new_file_name = file_name.translate(TRANS)
    other_file_name = ''
    for i in new_file_name:
        if i.isalnum() or i == '.':
            other_file_name += i
        else:
            i = '_'
            other_file_name += i
    return other_file_name
        

def create_dir(folder_path):        #I died when I worte this shit, this function is supposed to create directories and move files but it doesn't work!
    try:
        for i in all_folders:
            path = os.path.join(folder_path, i)
            os.makedirs(path, exist_ok=True)
            for file in all_adresses:
                file = Path(file)
                if file in archives:
                    name = file.stem
                    new_path = os.path.join(path, str(normalize(str(name))))
                    os.makedirs(new_path, exist_ok=True)
                    shutil.unpack_archive(file, new_path)
                elif file.name in all_folders:
                    continue
                else:
                    name = file.name
                    other_path = os.path.join(path, normalize(str(name)))
                    try:
                        shutil.move(file, other_path)
                    except:
                        continue
    except FileNotFoundError:
        print("Couldn't find a file")

def main(folder_path):
    path = folder_path
    sorting(path)
    create_dir(path)
    check_empty_dir(path)

#in this damn block you may see that I f*cked myself to do it through glob module. It almost worked but you may try to improve it
'''
def sorter(folder_path):    #here we create a function which will scan all extensions and add them to lists if it found
    path = str(folder_path)
    for i in extensions_we_sort.keys():
        for file in glob(path + f'\\**\\*.{i}', recursive=True):
            extensions_we_sort[i].append(file)
            known_extensions.add(f'{i}')
        for file in glob(path + '\\**\\*.*', recursive=True):
            if not str(file.endswith(str(i))):
                others.append(file)
                unknown_extensions.add(file[file.rindex('.') + 1:])
'''    

def check_empty_dir(path):       #this one seems to work, it deletes empty directories
    try:
        for i in os.listdir(path):
            p = os.path.join(path, i)
            if os.path.isdir(p):
                check_empty_dir(p)
                if not os.listdir(p):
                    os.rmdir(p)
    except PermissionError:
        print('It is fotbidden to  delete this directory')

if __name__ == '__main__':  #indicates that we are gonna use given files` name in the command line
    path = sys.argv[1]
    print(f'Start in {path}')

    arg = Path(path)
    main(arg.resolve())

    print(f"Images: {images}\n")
    print(f"Video: {video}\n")
    print(f"Audio: {audio}\n")
    print(f"Documents: {documents}\n")
    print(f"Archives: {archives}\n")
    print(f"Known extensions: {known_extensions}\n")
    print(f"Unknown extensions: {unknown_extensions}\n")