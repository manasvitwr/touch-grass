import subprocess
import csv
import datetime
import os
import win32gui
import win32process
import psutil
import time
import sys

def get_current_data():
    data = {'date': datetime.datetime.now()}

    try:
        # Get the handle of the foreground window
        hwnd = win32gui.GetForegroundWindow()

        # Get the window title
        title = win32gui.GetWindowText(hwnd)
        data['title'] = title

        # Get the process ID of the window
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        data['pid'] = pid

        # Use psutil to get process name/executable
        try:
            process = psutil.Process(pid)
            data['process_name'] = process.name()
            data['exe_path'] = process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            data['process_name'] = "Unknown"
            data['exe_path'] = "Unknown"

        # Use hwnd as XID equivalent and track time
        data['xid'] = hwnd
        data['timeactive'] = int(time.time())

        return data

    except Exception as e:
        print(f"Error getting window data: {e}")
        return None

def append_row(filename, data):
    if data is None:
        return

    row = [
        data['date'].strftime("%Y-%m-%d %H:%M:%S"),
        data['xid'],
        data['pid'],
        data['title'],
        data['process_name'],
        data.get('timeactive', None)
    ]

    today = datetime.datetime.now().strftime("%m-%d-%Y")
    csv_dir_name = 'csv_data'
    script_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(script_path, csv_dir_name)):
        os.mkdir(os.path.join(script_path, csv_dir_name))
    
    filepath = os.path.join(script_path, csv_dir_name, f'{filename}-{today}.csv')

    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(['Date', 'xid', 'pid', 'title', 'process', 'timeactive'])

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(row)

def continuous_tracking():
    """Run continuous tracking every 30 seconds"""
    print("Starting continuous activity tracking...")
    print("Tracking active window every 30 seconds")
    print("Press Ctrl+C to stop tracking")
    
    try:
        while True:
            current_data = get_current_data()
            if current_data:
                append_row('watch', current_data)
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] Tracked: {current_data['process_name']} - {current_data['title'][:50]}...")
            else:
                print("Failed to get current window data.")
            
            # Wait 30 seconds before next tracking
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nStopping activity tracker...")

if __name__ == '__main__':
    # If run with --continuous flag, run continuous tracking
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        continuous_tracking()
    else:
        # Original behavior - single log
        current_data = get_current_data()
        if current_data:
            append_row('watch', current_data)
            print(f"Logged: {current_data['process_name']} - {current_data['title']}")
        else:
            print("Failed to get current window data.")