import json
import time
import signal
import sys
from datetime import datetime
import argparse

# Spinner frames
frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

# Load or initialize the activity log
def load_activity_log():
    try:
        with open('activity_log.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: The activity log file is corrupted. Creating a new file.")
        return {}

def save_activity_log(log):
    try:
        with open('activity_log.json', 'w') as file:
            json.dump(log, file, indent=4)
    except IOError as e:
        print(f"Error: Unable to save activity log. {e}")

def start_timer(activity_name):
    categories = activity_name.split('/')
    start_time = time.time()
    print(f"Starting timer for {activity_name}. Press Ctrl+C to stop.")
    
    def signal_handler(sig, frame):
        end_time = time.time()
        elapsed_time = int((end_time - start_time) / 60)  # Convert to minutes
        log_time(activity_name, elapsed_time)
        print(f"\nStopped timer. Logged {elapsed_time} minutes for {activity_name}.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    i = 0
    while True:
        print(frames[i % len(frames)], end='\r')
        time.sleep(0.1)
        i += 1

def add_time(activity_name, minutes):
    try:
        minutes = int(minutes)
        if minutes < 0:
            raise ValueError("Minutes cannot be negative.")
        log_time(activity_name, minutes)
        print(f"Added {minutes} minutes to {activity_name}.")
    except ValueError as e:
        print(f"Error: {e}")

def log_time(activity_name, minutes):
    log = load_activity_log()
    categories = activity_name.split('/')
    current = log
    
    for category in categories:
        if category not in current:
            current[category] = {"time": 0, "timestamp": ""}
        current = current[category]
    
    current["time"] += minutes
    if current["timestamp"] == "":
        current["timestamp"] = datetime.now().isoformat()
    
    save_activity_log(log)

def print_activities():
    log = load_activity_log()
    print(json.dumps(log, indent=4))

def main():
    parser = argparse.ArgumentParser(description="Activity Tracker")
    parser.add_argument('-t', '--timer', type=str, help='Start a timer for an activity')
    parser.add_argument('-a', '--add', type=str, nargs=2, help='Add time manually to an activity')
    parser.add_argument('-l', '--list', action='store_true', help='List all activities and categories')
    
    args = parser.parse_args()
    
    if args.timer:
        start_timer(args.timer)
    elif args.add:
        activity_name, minutes = args.add
        add_time(activity_name, minutes)
    elif args.list:
        print_activities()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()