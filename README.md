Touch Grass is a Windows activity tracker for people who suspect they should probably touch grass a bit more often. It logs what you are actually doing on your PC, stores everything locally, and turns it into heatmaps, charts, and time‑series graphs so you can see where the day really went.

## Overview

Touch Grass watches which window is in focus on your machine and keeps a minute‑by‑minute (or sub‑minute) log of your activity. The UI then turns those logs into a graphical daily “story” of your screen time, with visual summaries that make it easy to recall, analyse, and, if needed, regret how you spent the day.

## Features

- **Activity Heatmap**: The Activity panel now renders a weekly heatmap: days on the X‑axis, hourly slots on the Y‑axis, with brightness showing how engaged you were in each block.
- **Focus vs Distraction**: A “Focus vs Distraction” summary panel breaks your day into Deep work, Admin & overhead, Distraction, and Off‑PC time, with a countdown until you hit your daily distraction cap.
- **App List Readability**: Process names are normalised for readability (comet.exe → Comet, social apps like WhatsApp and Instagram are detected from window titles and grouped under Distraction).
- **Local Logging**: Tracks active window title and process at a fixed interval (for example every 30 or 60 seconds) and logs each day to a local CSV file.
- **Reports**: Generates an HTML report with heatmaps, charts, and time graphs.


## Installation

1. Install Python 3.x and make sure `python` is available in your PATH.  
2. (Recommended) Create and activate a virtual environment in the project folder:  
   - `python -m venv venv`  
   - On Command Prompt: `venv\Scripts\activate`  
   Using a virtual environment keeps this project’s dependencies isolated from everything else.  
3. Clone this repository to a local folder.  
4. From the repository root (with the virtual environment activated, if you are using one), install dependencies:  
   - `pip install -r requirements.txt`  
5. Run `touch_grass.py` and `activity_report.py` once from a terminal to confirm everything works.

## Usage

### One‑off tracking session

- Start tracking the current session:  
  `python touch_grass.py`  
- When you are done, stop the script and generate a report for today:  
  `python activity_report.py`

### Continuous tracking with `--continuous`

- To keep logging running in the background all day, use:  
  `python touch_grass.py --continuous`  
- This mode is meant to be started automatically so you do not have to remember it every morning.

### Viewing previous days with `--daysago`

- To generate a report for a previous day:  
  `python activity_report.py --daysago N`  
- `N` is the number of days ago (for example, `--daysago 1` for yesterday, `--daysago 7` for the same weekday last week).

## Automating with Windows Task Scheduler

### Option 1: Task Scheduler UI

1. Open the Start menu, search for “Task Scheduler”, and launch it.  
2. In the “Actions” pane, click “Create Task…”.  
3. On the “General” tab, give it a name like `TouchGrass Continuous Logger` and select “Run only when user is logged on”.  
4. On the “Triggers” tab, click “New…”, set “Begin the task” to “At log on”, pick your user account, and save.  
5. On the “Actions” tab, click “New…”, set “Action” to “Start a program”, then:  
   - Program/script: path to `python.exe` (for example `C:\Users\<you>\AppData\Local\Programs\Python\Python39\python.exe`).  
   - Add arguments: `"<path-to-repo>\touch_grass.py" --continuous`  
   - Start in: the repo folder (for example `C:\Users\<you>\Projects\touch-grass`).  
6. Save the task. From the next logon onwards, Touch Grass will start tracking automatically.

### Option 2: Command‑line task using `schtasks`

1. Open Command Prompt as the user who should run the tracker.  
2. Create the task (edit paths and Python version as needed):  
   ```cmd
   schtasks /CREATE /SC ONLOGON /TN "TouchGrass\ContinuousLogger" ^
     /TR "\"C:\Path\To\Python\python.exe\" \"C:\Path\To\Repo\touch_grass.py\" --continuous" ^
     /RU "%USERNAME%"
   ```
3. Check that it exists:  
   ```cmd
   schtasks /QUERY /TN "TouchGrass\ContinuousLogger"
   ```

## Getting started with the helper batch files

To keep things as low‑effort as possible, the repo can include batch scripts so you manage logging and reports with a couple of double‑clicks instead of typing commands.

### Step 1 – Configure your Python path (optional but recommended)

- Open `create_touch_grass_task.bat` and `run_touch_grass_report.bat` in a text editor.  
- In both files, find the line that sets `PYTHON_PATH`.  
- If `python` already works in a terminal, leave it as `python.exe`.  
- If you use a specific interpreter or a virtual environment, point it to that instead, for example:  
  `C:\Users\<your-user>\Projects\touch-grass\venv\Scripts\python.exe`  
  This ensures the scheduled task and batch files use the same environment you installed dependencies into.

### Step 2 – Enable continuous tracking at logon

- Make sure `touch_grass.py` and `create_touch_grass_task.bat` live in the same folder.  
- Right‑click `create_touch_grass_task.bat` and choose “Run as administrator” (recommended) or double‑click it.  
- The script will create a scheduled task called `TouchGrass\ContinuousLogger` that runs `touch_grass.py --continuous` every time you log in.  
- Once it shows a success message, you can close the window; tracking is now on autopilot.

### Step 3 – Generate and open reports with a click

Once the logger has been running for a while, you can use a batch file to generate reports.

- To generate a report for **today**:  
  - Double‑click `run_touch_grass_report.bat`.  
  - It will run `activity_report.py` for today and open the HTML dashboard in your default browser (or drop the file where it normally does).

- To generate a report for **a previous day** using `--daysago`:  
  - Right‑click `run_touch_grass_report.bat` and choose “Create shortcut”.  
  - Edit the shortcut’s “Target” and add a number after the filename, for example:  
    `run_touch_grass_report.bat 1` (yesterday) or `run_touch_grass_report.bat 7` (last week).  
  - Double‑click that shortcut whenever you want that specific report.  
  - You can also run the batch directly from a terminal, for example:  
    `run_touch_grass_report.bat 1`

### Step 4 – Disable continuous tracking

- When you want to stop Touch Grass from starting at logon, double‑click `delete_touch_grass_task.bat`.  
- The script removes the `TouchGrass\ContinuousLogger` task and prints a confirmation before closing.


Set it up once, let it quietly watch your screen time, and then use the reports to decide whether you earned your right to not touch grass today—or whether it is time to close the browser and go outside 🍀

