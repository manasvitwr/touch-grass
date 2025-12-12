# Touch Grass

[![Built for Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://microsoft.com/windows)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![Privacy First](https://img.shields.io/badge/Privacy-Local_Storage_Only-green.svg)](#)

> **"Touch Grass"** is a detailed activity tracker that records your active window every 30 seconds and generates beautiful, interactive reports—so you can analyze (and sometimes regret) how you spend your digital life.

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#%EF%B8%8F-usage)
- [Project Structure](#-project-structure)
- [Configuration](#%EF%B8%8F-configuration)
- [Screenshots](#-screenshots)

## ✨ Features

- **High-Resolution Tracking**: Captures your active window title and process name every 30 seconds using native Win32 APIs.
- **Privacy-First Architecture**: Your data never leaves your machine. All logs are stored in local, human-readable CSV files in the `csv_data` folder.
- **Beautiful Visuals**: Generates an offline HTML dashboard with interactive D3.js charts to visualize your day.
- **Windows Native**: Optimized specifically for Windows environments.

## 🛠 Tech Stack

- **Core**: Python 3.x (`pywin32`, `psutil` for system monitoring).
- **Reporting**: HTML5, JavaScript (`D3.js` for charts), `Jinja2` (templating).
- **Storage**: CSV (Local file system).

## 🚀 Installation

### Prerequisites
- **OS**: Windows 10 or Windows 11.
- **Python**: Python 3.x installed and added to your system `PATH`.

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/touch-grass.git
    cd touch-grass
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🕹️ Usage

You can use the provided batch files for a one-click experience, or run commands manually.

### 1. Start Tracking
**Option A: Automatic (Recommended)**
Double-click `create_touch_grass_task.bat` to schedule the tracker to run automatically every time you log in.

**Option B: Manual**
Run the following command in your terminal:
```bash
python touch_grass.py --continuous
```
*Note: This will capture data every 30 seconds until you close the window.*

### 2. Stop Tracking
**Option A:**
Double-click `delete_touch_grass_task.bat` to remove the background task.

**Option B:**
If running manually, simply press `Ctrl+C` in the terminal window.

### 3. Generate Reports
**Option A: One-Click**
Double-click `run_touch_grass_report.bat`. This will generate today's report and open it in your browser.

**Option B: Manual Command**
To generate a report for today:
```bash
python activity_report.py
```

To generate a report for a specific number of days ago (e.g., 3 days ago):
```bash
python activity_report.py --daysago 3
```

## 📂 Project Structure

- `touch_grass.py`: The main tracking script that hooks into Win32 APIs.
- `activity_report.py`: The report generator that compiles CSV data into an HTML dashboard.
- `csv_data/`: Directory containing daily logs (e.g., `watch-MM-DD-YYYY.csv`).
- `web/`: Frontend assets (`index.html`, `d3pie.js`, CSS) for the dashboard.
- `*.bat`: Helper scripts for scheduling and reporting.

## ⚠️ Configuration

- **Data Storage**: Logs are stored in the `./csv_data` directory relative to the script.
- **Ignored Apps**: Currently, all active windows are logged.
- **Customization**: You can edit the batch files (`.bat`) to point to a specific Python executable if it's not in your global `PATH`.

## 📸 Screenshots

<div align="center">
    <img src="./assets/SS1.png" width="800px" alt="Dashboard Overview"/>
    <br/><br/>
    <img src="./assets/SS2.png" width="800px" alt="Activity Breakdown"/>
</div>

---

**Made with 💚 for those who need to touch grass.**
