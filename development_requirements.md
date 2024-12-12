# Activity Tracker Program Development Document

## **Overview**

### **Objective**

The goal is to build a Python-based activity tracking program that works in a Bash environment. The program will:

- Track time spent on activities.
- Organize activities into categories using a hierarchical structure (e.g., `linux/cmd-20`).
- Summarize time spent on categories and individual activities.
- Use JSON as the save file format for ease of use and flexibility.

### **Target Environment**

- Operating System: Linux
- Interface: Command-line (CLI)
- Dependency: Python 3.x
- Alias for Execution: `act`

---

## **Features**

### **Core Features**

1. **Start Timer for an Activity**

   - Command: `act -t "<category>/<activity>"`
   - Starts a real-time timer for the specified activity.
   - Automatically stops when interrupted (Ctrl+C) and logs the elapsed time.

2. **Add Time Manually**

   - Command: `act -a "<category>/<activity>" <minutes>`
   - Manually logs a specified number of minutes for an activity.

3. **List Activities and Categories**

   - Command: `act -l`
   - Displays a summary of all activities and total time spent in each category.
   - Displays categories and activities in a nested format similar to the `tree` command.
   - Includes optional color-coded output for better readability.

4. **Support for Nested Categories**

   - Activities can have multiple levels of categories (e.g., `game/pathfinder/society`).
   - Summarizes time for each level of the hierarchy (e.g., total for `game`, `game/pathfinder`, etc.).
   - Unlimited depth for nested categories.

5. **Timestamps for Activities**

   - Records the timestamp of when an activity was first started.
   - Displays timestamps when listing activities.
   - Timestamps remain as the first entry's time for each activity.

### **Planned Enhancements**

- **Export Data**: Export activity data to CSV for analysis.
- **Reporting**: Generate weekly or monthly summaries, including daily review reports.
- **Error Handling**: Graceful handling of incorrect inputs.

---

## **Save File Format**

### **Format: JSON**

JSON is chosen for its readability, flexibility, and hierarchical support.

#### **Example File Structure**

```json
{
    "linux": {
        "cmd-19": {
            "time": 33,
            "timestamp": "2023-12-01T10:00:00"
        },
        "cmd-20": {
            "time": 25,
            "timestamp": "2023-12-02T14:30:00"
        },
        "total": 58
    },
    "game": {
        "pathfinder": {
            "society": {
                "time": 182,
                "timestamp": "2023-12-03T18:45:00"
            },
            "total": 182
        },
        "total": 182
    },
    "total": 240
}
```

#### **Advantages**

- **Human-readable**: Easily editable by users.
- **Scalable**: Supports nested categories and detailed tracking.
- **Easy Parsing**: Directly parseable with Python’s `json` module.

---

## **Technical Design**

### **Dependencies**

- Python 3.x
- Modules: `json`, `argparse`, `time`, `datetime`, `signal`, `colorama` (optional for colored output)

### **Directory Structure**

```
activity_tracker/
├── activity_tracker.py   # Main script
└── activity_log.json    # Save file
```

### **Core Functions**

#### 1. `start_timer(activity_name)`

- **Purpose**: Tracks time for a specified activity in real-time.
- **Workflow**:
  1. Parse `activity_name` into categories and activity.
  2. Start a timer and display a spinner.
  3. On interrupt, calculate elapsed time and log it.
  4. Record the current timestamp if it’s the first log for this activity.
  5. Update totals in the JSON file for all hierarchical levels.

#### 2. `add_time(activity_name, minutes)`

- **Purpose**: Adds a specified duration to an activity.
- **Workflow**:
  1. Parse `activity_name` into categories and activity.
  2. Add `minutes` to the activity and update category totals.
  3. Record the current timestamp if it’s the first log for this activity.
  4. Save updated data to the JSON file.

#### 3. `print_activities()`

- **Purpose**: Lists all activities, their times, and timestamps.
- **Workflow**:
  1. Read the JSON save file.
  2. Display each category, its activities, their times, and timestamps in a structured nested format.
  3. Optionally, color-code categories and activities for better readability.

### **Command-Line Argument Parsing**

- **Library**: `argparse`
- **Commands**:
  - `-t, --timer`: Start a timer for an activity.
  - `-a, --add`: Manually log time for an activity.
  - `-l, --list`: List all activities and totals.

---

## **Example Usage**

### **1. Start Timer for an Activity**

Command:

```bash
act -t "game/pathfinder/society"
```

Expected Output:

```
Tracking time for: game/pathfinder/society
⢿ (spinner animation)
Time spent: 33 minute(s).
```

### **2. Add Time Manually**

Command:

```bash
act -a "linux/cmd-20" 45
```

Expected Output:

```
Added 45 minutes to linux/cmd-20.
```

### **3. List Activities**

Command:

```bash
act -l
```

Expected Output:

```
Activity                 | Time Spent (minutes) | Timestamp
-----------------------------------------------------------
linux/cmd-19            | 33                   | 2023-12-01T10:00:00
linux/cmd-20            | 70                   | 2023-12-02T14:30:00
linux (total)           | 103                  |
game/pathfinder/society | 182                  | 2023-12-03T18:45:00
game/pathfinder (total) | 182                  |
game (total)            | 182                  |
-----------------------------------------------------------
Total                   | 240                  |
```

---

## **Error Handling**

### **Common Errors and Solutions**

1. **Invalid Command**:

   - **Cause**: User enters an unsupported command.
   - **Solution**: Display help message using `argparse`.

2. **Invalid Input Format**:

   - **Cause**: Activity name or minutes is not correctly formatted.
   - **Solution**: Validate input and provide clear error messages.

3. **File Not Found or Corruption**:

   - **Cause**: Save file is missing, corrupted, or contains invalid JSON.
   - **Solution**: Automatically create a new save file or attempt to repair the corrupted file.

4. **Performance Issues with Large Data Sets**:

   - **Cause**: JSON file grows too large, slowing down parsing and updates.
   - **Solution**: Introduce archiving or indexing mechanisms for old data.

---

## **Testing Plan**

### **Unit Tests**

- Test functions like `add_time` and `start_timer` with mock inputs.

### **Integration Tests**

- Simulate user inputs via CLI to verify end-to-end functionality.

### **Edge Cases**

- Activity names with special characters.
- Summing across multiple categories.
- Handling empty or corrupted JSON files.

---

## **Future Enhancements**

1. **Subcategories**:

   - Add nested subcategories for deeper organization.

2. **Web Interface**:

   - Create a simple web app for managing activities.

3. **Integration with Tools**:

   - Export data to Google Sheets or other productivity tools.

4. **Indexing for Large Data Sets**:

   - Implement indexing or archiving to optimize performance with large JSON files.

5. **Environment Setup**:

   - Introduce `requirements.txt` or `pyproject.toml` for dependency management.

6. **Color-Coded CLI Output**:

   - Use libraries like `colorama` to enhance the visual output of the CLI.

---

## **Conclusion**

This activity tracker leverages Python’s simplicity and JSON’s flexibility to provide a robust and user-friendly solution for tracking time spent on various activities. It’s designed to grow with additional features while remaining lightweight and portable.

Let me know if you need further clarification or want to start implementation!

