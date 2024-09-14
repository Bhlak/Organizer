mapping = {
        "pdf": "Docs",
        "txt": "Docs",
        "pptm": "Docs",
        "docx": "Docs",
        "xlsx": "Docs",
        "pptx": "Docs",
        "pptm": "Docs",

        "png": "Images",
        "jpg": "Images",
        "JPG": "Images",
        "jpeg": "Images",

        "html": "Webpages",

        "mp3": "Music/Sounds",
        
        "deb": "Programs",
        "AppImage": "Programs",
        "exe": "Programs",
        
        "gz": "Compressed",
        "xz": "Compressed",
        "zip": "Compressed",
        
        "mp4": "Videos",
        "webp": "Videos",
        
        "sh": "Bash",

        "gb": "ROM Images",

        "py": "Code",

        "db": "Database Files"
    }

def organizer(path):
    from os import listdir
    from os.path import isfile, join
    
    files = [f for f in listdir(path) if isfile(join(path, f))]
    
    for i in files:
        filetype = i.split('.')[-1]

        # with open(f'{path}/temp.txt', 'a+') as f:
        #     f.seek(0)
        #     types = f.readlines()
        #     if f'{filetype}\n' in types:
        #         continue
        #     f.writelines(f'{filetype}\n')

        sorter(path=path, file=i, type=filetype)


def get_folder(type):
    if type not in mapping:
        return None
    return mapping[type] 
    


def sorter(path, file, type):
    import os
    import shutil

    dest = get_folder(type)
    
    if dest:
        newpath = os.path.join(path, dest)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        try:
            shutil.move(os.path.join(path, file), os.path.join(newpath, file))
        except Exception as e:
            with open(f'{path}/report.txt', 'a+') as f:
                f.write(f"Error Encountered: {e} \n")
        
        return True

        

    return None



if __name__ == '__main__':
    organizer("/home/bhlak/Downloads")