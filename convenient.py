def load_schedule():
    import os
    import json

    sched_file = os.path.join(get_user_data_dir(), "schedule.json")
    if not os.path.exists(sched_file):
        default_schedule = {"type": "daily", "every": 1, "time": "00:00", "weekday": "monday"}
        with open(sched_file, "w") as f:
            json.dump(default_schedule, f)
        return default_schedule

    try:
        with open(sched_file, "r") as f:
            return json.load(f)
    except Exception as e:
        return None
    
        
def load_folders():
    import os
    folder_file = os.path.join(get_user_data_dir(), "folders.txt")
    
    if os.path.exists(folder_file):
        try:
            with open(folder_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("No folders.txt found!")
            return []


def add_to_startup():
    import os
    import sys
    
    try:
        from win32com.client import Dispatch
    except ImportError:
        print("Error: pywin32 is required to add_to_startup()")
        return

    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )

    # task_cmd = f'"{pythonw}" "{executor_path}"'

    shortcut_path = os.path.join(startup_folder, "Organizer.lnk")
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    if getattr(sys, 'frozen', False):
        args = ""
        # target = sys.executable
        base_dir = os.path.dirname(sys.executable)
        exe_path = os.path.join(base_dir, "Executor.exe")
   
        shortcut.TargetPath = exe_path
        shortcut.Arguments = args
        shortcut.WorkingDirectory = base_dir
        shortcut.IconLocation = exe_path
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        py_path = os.path.join(base_dir, "executor.py")
    
        target = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(target):
            target = sys.executable

        shortcut.TargetPath = pythonw
        shortcut.Arguments = f'"{py_path}"'
        shortcut.WorkingDirectory = base_dir
        shortcut.IconLocation = pythonw
    shortcut.save()

def resource_path(relative_path):
    import sys, os

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_user_data_dir():
    import os
    import sys

    if getattr(sys, 'frozen', False):
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        data_dir = os.path.join(base, "OrganizerApp")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base)

    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_defaults():
    import os, sys

    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    
    default_dir = os.path.join(base_dir, "defaults")
    return default_dir

def ensure_config_file(filename):
    import os
    import shutil

    user_dir = get_user_data_dir()
    default_path = get_defaults()
    default_file = os.path.join(default_path, filename)
    user_file =  os.path.join(user_dir, filename)
    if (not os.path.exists(user_file)) and os.path.exists(default_file):
        shutil.copy(default_file, user_file)
    return user_file

def log(msg):
    import os
    import time

    # base_dir = get_user_data_dir()
    # log_file = os.path.join(base_dir, "debug_log.txt")
    log_file = ensure_config_file("debug_log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def stop_autorun():
    import os, schedule, json, shutil, platform, subprocess
    from convenient import get_user_data_dir, ensure_config_file

    sched_file = ensure_config_file("schedule.json")
    with open(sched_file, "w") as f:
        json.dump({}, f)

    if platform.system() == "Windows":
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(
                ["taskkill", "/IM", "executor.exe", "/T", "/F"], 
                check=False,
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW
                )
        except Exception:
            pass
    
    startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    shortcut = os.path.join(startup_dir, "Organizer.lnk")
    if os.path.exists(shortcut):
        os.remove(shortcut)
    
    return True
