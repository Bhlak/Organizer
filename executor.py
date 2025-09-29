import os, sys, time, schedule, datetime, json
from convenient import (
    load_schedule, load_folders, 
    ensure_config_file, get_user_data_dir, resource_path
                        )

last_run_file = os.path.join(get_user_data_dir(), "last_run.json")

def log(msg):
    # base_dir = get_user_data_dir()
    log_file = ensure_config_file("executor_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_last_run():
    if os.path.exists(last_run_file):
        with open(last_run_file, "r") as f:
            try:
                data = json.load(f)
                return datetime.datetime.fromisoformat(data.get("last_run"))
            except Exception:
                return None
    return None

def save_last_run(stamp=None):
    stamp = stamp or datetime.datetime.now()
    with open(last_run_file, "w") as f:
        json.dump({"last_run": stamp.isoformat()}, f)

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

def should_catch_up(schedule_data, last_run, now):
    if not schedule_data or "type" not in schedule_data:
        return False
    
    sched_type = schedule_data.get("type")
    sched_time_str = schedule_data.get("time", "00:00")
    sched_time = datetime.datetime.strptime(sched_time_str, "%H:%M").time()

    check_day = (last_run or (now - datetime.timedelta(days=1))).date()
    while check_day <= now.date():
        candidate = datetime.datetime.combine(check_day, sched_time)

        if sched_type == "daily":
            if candidate > (last_run or candidate) and candidate <= now:
                return True
        elif sched_type == "weekly":
            weekday = schedule_data.get("weekday", "monday").lower()
            weekday_map = {
                "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                "friday": 4, "saturday": 5, "sunday": 6
            }
            if check_day.weekday() == weekday_map.get(weekday, 0):
                if candidate > (last_run or candidate) and candidate <= now:
                    return True
        elif sched_type == "monthly":
            every = int(schedule_data.get("every", 1))
            if (now - check_day).days >= 0 and (now - check_day).days % (every * 30) == 0:
                if candidate > (last_run or candidate) and candidate <= now:
                    return True
                
        check_day += datetime.timedelta(days=1)
    return False

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
    sched_file = ensure_config_file("schedule.json")
    
    now = datetime.datetime.now()
    last_run = load_last_run()
    schedule_data = load_schedule()

    if should_catch_up(schedule_data, last_run, now):
        log("Missed scheduled run detected, running catch-up task...")
        run_organizer()
    save_last_run(now)

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