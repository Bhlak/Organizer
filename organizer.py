def log(msg):
    import os
    import time
    from convenient import ensure_config_file

    log_file = ensure_config_file("organizer_log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def organizer(path):
    from os import listdir
    from os.path import isfile, join
    from convenient import log as debug_log
    from organizer import sorter, log as organizer_log


    files = [f for f in listdir(path) if isfile(join(path, f))]

    for i in files:
        filetype = i.split('.')[-1].lower()
        try:
            sorter(path=path, file=i, type=filetype)
        except Exception as e:
            organizer_log(f"Organizer Error: {e}")
            organizer_log(f"Path: {path}")
            organizer_log(f"File: {i}")
            organizer_log(f"Extension: {filetype}")
            continue

def get_folder(type):
    from convenient import load_mappings
    from convenient import log as debug_log

    mapping = load_mappings()
    type = type.lower()
    for folder, extensions in mapping.items():
        if type in [extension.lower() for extension in extensions]:
            return folder
    return None

def sorter(path, file, type):
    import os
    import shutil
    from convenient import get_user_data_dir
    from convenient import log as debug_log


    dest = get_folder(type)
    
    temp = os.path.join(path, dest)
    if dest:
        newpath = os.path.join(path, dest)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        try:
            shutil.move(os.path.join(path, file), os.path.join(newpath, file))
        except Exception as e:
                debug_log(f"Error: {e}\n")
        return True
    return None

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        organizer(folder)