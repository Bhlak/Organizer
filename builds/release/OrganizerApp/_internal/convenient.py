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

    if getattr(sys, 'frozen', False):
        args = ""
        target = sys.executable
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        target = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(target):
            target = sys.executable
        args = f'"{os.path.join(base_dir, "executor.py")}"'

    exe_path = os.path.join(base_dir, "Executor.exe")
    py_path = os.path.join(base_dir, "executor.py")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    if os.path.exists(exe_path):
        shortcut.TargetPath = exe_path
        shortcut.Arguments = args
        shortcut.WorkingDirectory = base_dir
        shortcut.IconLocation = exe_path
    elif os.path.exists(py_path):
        pythonw = os.path.join(sys.prefix, "Scripts", "pythonw.exe")
        if not os.path.exists(pythonw):
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
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

def ensure_config_file(filename, default_path):
    import os
    import shutil

    user_dir = get_user_data_dir()
    user_file =  os.path.join(user_dir, filename)
    if (not os.path.exists(user_file)) and os.path.exists(default_path):
        shutil.copy(default_path, user_file)
    return user_file

def log(msg):
    import os
    import time

    base_dir = get_user_data_dir()
    # log_file = os.path.join(base_dir, "debug_log.txt")
    log_file = ensure_config_file("debug_log.txt", resource_path("defaults/debug_log.txt"))

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")



# def register_task():
#     import sys, os, subprocess

#     pythonw = os.path.join(sys.prefix, "Scripts", "pythonw.exe")
#     executor_path = resource_path("executor.exe" if getattr(sys, 'frozen', False) else "executor.py")
#     task_name = "OrganizerScheduler"
#     task_cmd = f'"{pythonw}" "{executor_path}"'

#     cmd = [
#         "schtasks", "/Create",
#         "/SC", "ONLOGON",
#         "/TN", task_name,
#         "/TR", task_cmd,
#         "/RL", "LIMITED",
#         "/RU", os.getlogin(),
#         "/F"
#     ]

#     try:
#         subprocess.run(["schtasks", "/Delete", "/TN", task_name, "/F"], check=False)
#         subprocess.run(cmd, check=True)
#     except subprocess.CalledProcessError as e:
#         print("Failed to create scheduled task:", e)

# def get_data_dir():
#     import os
#     import sys
#     if getattr(sys, 'frozen', False):
#         base_dir = os.path.join(os.environ["APPDATA"], "OrganizerApp")
#     else:
#         base_dir = os.path.abspath(os.path.dirname(__file__))
#     os.makedirs(base_dir, exist_ok=True)
#     return base_dir
