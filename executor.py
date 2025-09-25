import os
import sys
import time
import schedule
from convenient import (
    load_schedule, load_folders, 
    ensure_config_file, get_user_data_dir, resource_path
                        )


def log(msg):
    base_dir = get_user_data_dir()
    log_file = ensure_config_file("executor_log.txt", resource_path("defaults/executor_log.txt"))

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def run_organizer():
    import subprocess, platform, sys, os
    from organizer import organizer

    log("run_organizer called")
    folders = load_folders()
    if not folders:
        log("No folders loaded, exiting...")
        return
    
    for f in folders:
        log(f"Launching organizer.py for folder: {f}")
        try:
            organizer(f)
        except Exception as e:
            log(f"Failed to launch organizer.py for {f}: {e}")

def log_pending():
    for job in schedule.jobs:
        log(f" {job}")

def setup_schedule():
    log("setup_schedule called")
    schedule.clear()
    weekday_map = {
    "monday": schedule.every().monday,
    "tuesday": schedule.every().tuesday,
    "wednesday": schedule.every().wednesday,
    "thursday": schedule.every().thursday,
    "friday": schedule.every().friday,
    "saturday": schedule.every().saturday,
    "sunday": schedule.every().sunday,
}

    schedule_data = load_schedule()
    if not schedule_data:
        log("No schedule data found")
        return
    
    schedule_type = schedule_data.get("type", "daily")
    every = int(schedule_data.get("every", 1))
    time = schedule_data.get("time", "00:00")

    log(f"Schedule loaded: {schedule_data}")

    if schedule_type == "daily":
        schedule.every(every).days.at(time).do(run_organizer)
    elif schedule_type == "weekly":
        weekday = schedule_data.get("weekday", "monday").lower()
        if weekday in weekday_map:
            weekday_map[weekday].at(time).do(run_organizer)
    elif schedule_type == "monthly":
        schedule.every(every * 30).days.at(time).do(run_organizer)

    log_pending()

if __name__ == "__main__":

    log("executor.py started")
    sched_file = ensure_config_file("schedule.json", resource_path("defaults/schedule.json"))
    last_mod_time = None
    while True:
        try:
            if os.path.exists(sched_file):
                mod_time = os.path.getmtime(sched_file)
                if last_mod_time is None or mod_time != last_mod_time:
                    setup_schedule()
                    if mod_time != last_mod_time:
                        log("Schedule Changed")
                    last_mod_time = mod_time
            schedule.run_pending()
        except Exception as e:
            log(f"ERROR: {e}")
        time.sleep(5)