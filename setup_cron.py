def setup_windows_task():
    """
    Sets up a Windows scheduled task to run the activity tracker every 5 minutes.
    Returns True if successful, False if failed or already exists.
    """
    try:
        import win32com.client
        import pythoncom
        from datetime import datetime, timedelta
        
        # Initialize COM
        pythoncom.CoInitialize()
        
        # Connect to Task Scheduler
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        
        # Get root folder
        root_folder = scheduler.GetFolder('\\')
        
        # Check if task already exists
        task_name = 'ActivityTracker'
        try:
            existing_task = root_folder.GetTask(task_name)
            print("Windows scheduled task already exists.")
            return False
        except:
            pass  # Task doesn't exist, continue with creation
        
        # Create new task
        task_def = scheduler.NewTask(0)
        
        # Create trigger (every 5 minutes)
        trigger = task_def.Triggers.Create(1)  # TASK_TRIGGER_TIME
        trigger.Repetition.Interval = "PT5M"  # Repeat every 5 minutes
        trigger.StartBoundary = (datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S')
        trigger.Enabled = True
        
        # Create action (run the Python script)
        action = task_def.Actions.Create(0)  # TASK_ACTION_EXEC
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'touch_grass.py')
        python_exe = sys.executable  # Use the same Python that's running this script
        
        action.Path = python_exe
        action.Arguments = f'"{script_path}"'
        
        # Set settings
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False
        task_def.Settings.DisallowStartIfOnBatteries = False
        task_def.Settings.WakeToRun = False
        task_def.Settings.Priority = 7  # Normal priority
        
        # Register task (this might require admin privileges)
        try:
            root_folder.RegisterTaskDefinition(
                task_name,
                task_def,
                6,  # TASK_CREATE_OR_UPDATE
                None,  # No user
                None,  # No password
                1  # TASK_LOGON_INTERACTIVE_TOKEN
            )
            print("Windows scheduled task created successfully.")
            return True
        except Exception as admin_error:
            print(f"Note: Automatic task scheduling requires admin rights. Running in manual mode.")
            print(f"Admin error: {admin_error}")
            return False
        
    except Exception as e:
        print(f"Note: Running in manual mode. Automatic scheduling not available.")
        print(f"Scheduler error: {e}")
        return False
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass