import json
import time
import signal
import sys
from datetime import datetime
import argparse
import os

# Spinner frames
frames = ["⣾ ", "⣽ ", "⣻ ", "⢿ ", "⡿ ", "⣟ ", "⣯ ", "⣷ "]

# Path to the activity log file
activity_log_path = os.path.expanduser('~/Documents/activity_log.json')

# Load or initialize the activity log
def load_activity_log():
    try:
        with open(activity_log_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: The activity log file is corrupted. Creating a new file.")
        return {}

def save_activity_log(log):
    try:
        with open(activity_log_path, 'w') as file:
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
    while True:
        for frame in frames:
            sys.stdout.write(f"\r{frame} ")
            sys.stdout.flush()
            time.sleep(0.25)

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
    print_activity_tree(log)

def print_activity_tree(log, indent=0):
    for key, value in log.items():
        if isinstance(value, dict):
            time = value.get("time", 0)
            print(" " * indent + f"{key} ({time} minutes)")
            print_activity_tree(value, indent + 4)

def add_time(category_path, time):
    log = load_activity_log()
    categories = category_path.split('/')
    
    # Convert time to integer
    time = int(time)
    
    # Initialize the current level in the log
    current_level = log
    
    # Iterate through the categories and update the time
    for i in range(len(categories)):
        category = categories[i]
        if category not in current_level:
            current_level[category] = {"time": 0}
        
        # Add time to the current category
        current_level[category]["time"] += time
        
        # Move to the next level
        current_level = current_level[category]
    
    save_activity_log(log)

def delete_entry(log, entry_path):
    parts = entry_path.split('/')
    current = log
    stack = []

    for part in parts[:-1]:
        if part in current:
            stack.append((current, part))
            current = current[part]
        else:
            print(f"Entry '{entry_path}' not found.")
            return

    if parts[-1] in current:
        del current[parts[-1]]
        print(f"Entry '{entry_path}' deleted.")
    else:
        print(f"Entry '{entry_path}' not found.")

    # Clean up any empty parent entries
    while stack:
        parent, part = stack.pop()
        if not parent[part]:
            del parent[part]
        else:
            break

    # Clean up any empty nested dictionaries
    def clean_empty_entries(d):
        keys_to_delete = [k for k, v in d.items() if isinstance(v, dict) and not v]
        for k in keys_to_delete:
            del d[k]
        for v in d.values():
            if isinstance(v, dict):
                clean_empty_entries(v)

    clean_empty_entries(log)

def prompt_delete_entry():
    log = load_activity_log()
    entry_path = input("Enter the name of the entry to delete: ")
    delete_entry(log, entry_path)
    save_activity_log(log)

def main():
    parser = argparse.ArgumentParser(description="Activity Tracker")
    parser.add_argument('-t', '--timer', type=str, help='Start a timer for an activity')
    parser.add_argument('-a', '--add', type=str, nargs=2, help='Add time manually to an activity')
    parser.add_argument('-l', '--list', action='store_true', help='List all activities and categories')
    parser.add_argument("--delete", action="store_true", help="Delete an activity entry")
    
    args = parser.parse_args()
    
    if args.timer:
        start_time = time.time()
        start_timer(args.timer)
    elif args.add:
        activity_name, minutes = args.add
        add_time(activity_name, minutes)
        print(f"Added {minutes} minutes to {activity_name}")
    elif args.list:
        log = load_activity_log()
        print_activity_tree(log)
    elif args.delete:
        prompt_delete_entry()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()