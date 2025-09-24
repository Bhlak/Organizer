def load_schedule():
    import os
    import json

    sched_file = os.path.join(get_data_dir(), "schedule.json")

    if os.path.exists(sched_file):
        try:
            with open(sched_file, "r") as f:
                return json.load(f)
        except Exception as e:
            return None
    return None
        
def load_folders():
    import os
    folder_file = os.path.join(get_data_dir(), "folders.txt")
    
    if os.path.exists(folder_file):
        try:
            with open(folder_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("No folders.txt found!")
            return []

def register_task():
    import sys, os, subprocess

    pythonw = os.path.join(sys.prefix, "Scripts", "pythonw.exe")
    executor_path = resource_path("executor.exe" if getattr(sys, 'frozen', False) else "executor.py")
    task_name = "OrganizerScheduler"
    task_cmd = f'"{pythonw}" "{executor_path}"'

    cmd = [
        "schtasks", "/Create",
        "/SC", "ONLOGON",
        "/TN", task_name,
        "/TR", task_cmd,
        "/RL", "LIMITED",
        "/RU", os.getlogin(),
        "/F"
    ]

    try:
        subprocess.run(["schtasks", "/Delete", "/TN", task_name, "/F"], check=False)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to create scheduled task:", e)

def add_to_startup():
    import os
    import sys
    from win32com.client import Dispatch

    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )

    # task_cmd = f'"{pythonw}" "{executor_path}"'

    shortcut_path = os.path.join(startup_folder, "Organizer.lnk")

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    exe_path = os.path.join(base_dir, "executor.exe")
    py_path = os.path.join(base_dir, "executor.py")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    if os.path.exists(exe_path):
        shortcut.TargetPath = exe_path
        shortcut.Arguments = ""
        shortcut.WorkingDirectory = base_dir
        shortcut.IconLocation = exe_path
    elif os.path.exists(py_path):
        pythonw = os.path.join(sys.prefix, "Scripts", "pythonw.exe")
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

def get_data_dir():
    import os
    import sys
    if getattr(sys, 'frozen', False):
        base_dir = os.path.join(os.environ["APPDATA"], "OrganizerApp")
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(base_dir, exist_ok=True)
    return base_dir