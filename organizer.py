mapping = {
        "pdf": "Docs",
        "txt": "Docs",
        "docx": "Docs",
        "xlsx": "Docs",
        "pptx": "Docs",
        "pptm": "Docs",

        "cbz": "Comics",
        "cbr": "Comics",

        "png": "Images",
        "jpg": "Images",
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
        "mkv": "Videos",
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
        filetype = i.split('.')[-1].lower()
        sorter(path=path, file=i, type=filetype)

def get_folder(type):
    from convenient import load_mappings

    mapping = load_mappings()
    if type not in mapping:
        return None
    return mapping[type]

def sorter(path, file, type):
    import os
    import shutil
    from convenient import get_user_data_dir

    report_file = os.path.join(get_user_data_dir(), "organizer_log.txt")
    dest = get_folder(type)
    
    if dest:
        newpath = os.path.join(path, dest)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        try:
            shutil.move(os.path.join(path, file), os.path.join(newpath, file))
        except Exception as e:
            with open(report_file, 'a+', encoding="utf-8") as f:
                f.write(f"[{path}] Error: {e}\n")
        return True
    return None

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        organizer(folder)