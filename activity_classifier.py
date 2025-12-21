
SYSTEM_PROCESSES = {
    "screenclippinghost.exe",
    "snippingtool.exe",
    "systemsettings.exe",
    "control.exe",
    "explorer.exe",
    "searchapp.exe",
    "startmenuexperiencehost.exe",
    "applicationframehost.exe",
    "shellexperiencehost.exe",
    "taskmgr.exe",
}

SYSTEM_TITLE_KEYWORDS = [
    "settings",
    "control panel",
    "file explorer",
    "file manager",
    "snip & sketch",
    "task manager",
]

# Categorization Maps
DEEP_WORK_APPS = {
    "code.exe", "pycharm", "idea", "studio", "nvim", "vim", "sublime_text",
    "notepad++.exe", "obsidian.exe", "winword.exe", "excel.exe", "powerpnt.exe",
    "cmd.exe", "powershell.exe", "windowsterminal.exe", "mintty.exe",
    "antigravity.exe", "comet.exe", "touch_grass.py" 
}

# Distraction apps that are identifiable by process name
DISTRACTION_APPS = {
    "spotify.exe", "discord.exe", "steam.exe", "vlc.exe", 
    "netflix", "hulu", "prime", "youtube", "twitter", "reddit"
}

ADMIN_APPS = {
    "outlook.exe", "teams.exe", "slack.exe", "thunderbird.exe", "zoom.exe"
}

SOCIAL_KEYWORDS = [
    "whatsapp", "instagram", "discord",
    "pinterest", "twitter", "x.com",
    "reddit", "youtube", "tiktok",
    "facebook", "messenger"
]

# Browsers often need title analysis, but we'll default to Distraction for safety if unknown contents
BROWSERS = {"chrome.exe", "firefox.exe", "msedge.exe", "opera.exe", "brave.exe"}

def is_system_process(row):
    """
    Check if the row represents a system/utility process (Settings, Snipping Tool, etc.).
    Does NOT include LockApp (handled separately).
    """
    process = row.get('process', '').lower().strip()
    title = row.get('title', '').lower().strip()
    
    if process in SYSTEM_PROCESSES:
        return True
        
    for keyword in SYSTEM_TITLE_KEYWORDS:
        if keyword in title:
            return True
            
    return False

def is_off_pc(row):
    """Check if the row is Lock Screen (LockApp.exe)."""
    process = row.get('process', '').lower().strip()
    return process == "lockapp.exe"

def is_unknown(row):
    """Check if the row is Unknown/Empty."""
    process = row.get('process', '').lower().strip()
    return not process or process == "unknown"

def get_social_app_name(row):
    """
    Check if the row corresponds to a social app based on keywords.
    Returns the capitalized keyword as the App Name if found, else None.
    """
    title = row.get('title', '').lower().strip()
    process = row.get('process', '').lower().strip()
    
    # Check title first (often more descriptive for web apps)
    for kw in SOCIAL_KEYWORDS:
        if kw in title:
            # Map x.com to Twitter
            if kw == "x.com": return "Twitter"
            return kw.capitalize()
            
    # Check process name
    for kw in SOCIAL_KEYWORDS:
        if kw in process:
            if kw == "x.com": return "Twitter"
            return kw.capitalize()
            
    return None

def classify_activity(row):
    """
    Classify activity into:
    - 'off_pc' (LockApp)
    - 'unknown'
    - 'system' (Excluded utilities) -> Now 'admin' (Overhead)
    - 'deep_work'
    - 'admin'
    - 'distraction'
    
    Returns:
        (category, app_name)
    """
    process = row.get('process', '').lower().strip()
    title = row.get('title', '').lower().strip()

    # 1. Off PC
    if is_off_pc(row):
        return 'off_pc', 'LockApp'
    
    # 2. Unknown
    if is_unknown(row):
        return 'unknown', 'Unknown'

    # 3. Social / Distraction Keywords (High Priority for classification)
    social_name = get_social_app_name(row)
    if social_name:
        return 'distraction', social_name

    # 4. System / Overhead -> Now counts as ADMIN
    if is_system_process(row):
        return 'admin', process # or 'System Overhead'

    # 5. Deep Work
    if process in DEEP_WORK_APPS:
        return 'deep_work', process
    
    # 6. Explicit Admin Apps
    if process in ADMIN_APPS:
        return 'admin', process
        
    # 7. Explicit Distraction Processes
    if process in DISTRACTION_APPS:
        return 'distraction', process
    
    # 8. Browsers - Heuristics
    if process in BROWSERS:
        # Simple keywords in title
        if any(kw in title for kw in ["docs", "github", "stackoverflow", "jira", "linear", "notion"]):
            return 'deep_work', process
        if any(kw in title for kw in ["mail", "calendar", "meet"]):
            return 'admin', process
        return 'distraction', process # Default to distraction for browsers
        
    # Default fallback
    return 'distraction', process
