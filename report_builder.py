import os
from jinja2 import Environment, FileSystemLoader
import shutil
from datetime import datetime, timedelta
import json

from utils import readcsv, readjson
from activity_classifier import is_system_process


def report_builder(date, range_days=7):
    script_path = os.path.dirname(os.path.abspath(__file__))
    csv_file = f'watch-{date}.csv'

    if not os.path.exists( os.path.join(script_path, 'csv_data', csv_file ) ):
        return False

    shutil.copy2(os.path.join( script_path, 'csv_data', csv_file), os.path.join( script_path , 'web') )

    report_date = datetime.strptime(date, '%m-%d-%Y')
    report_date_str = report_date.strftime("%A ") + str(report_date.day) + report_date.strftime(" %B %Y")
    generation_date = datetime.now().strftime('%d %B %Y %H:%M')
    

    csv_data = readcsv(os.path.join(script_path, 'csv_data', csv_file ) )
    
    # Process data: Filter, Classify, and Aggregate
    from activity_classifier import classify_activity
    
    valid_rows = []
    off_pc_rows = []
    
    deep_work_mins = 0
    admin_mins = 0
    distraction_mins = 0
    off_pc_mins = 0
    
    # Each row is ostensibly ~30 seconds or 1 minute.
    INTERVAL_MINS = 0.5
    
    for row in csv_data:
        category, app_name = classify_activity(row)
        
        # CLEANUP APP NAME
        # Strip extension if present
        if app_name.lower().endswith('.exe'):
            app_name = app_name[:-4]
        # Capitalize
        app_name = app_name.capitalize()
        # Some manual enhances
        if app_name.lower() == 'code': app_name = 'VS Code'
        if app_name.lower() == 'idea': app_name = 'IntelliJ'
        
        # Update row with the cleaner app name for frontend display
        row['process'] = app_name
        
        if category == 'off_pc':
            off_pc_rows.append(row)
            off_pc_mins += INTERVAL_MINS
        elif category == 'unknown':
            # Completely ignored
            pass
        elif category == 'system':
            # Ignored from totals (though now system maps to admin usually)
            pass
        else:
            # User facing app
            valid_rows.append(row)
            if category == 'deep_work':
                deep_work_mins += INTERVAL_MINS
            elif category == 'admin':
                admin_mins += INTERVAL_MINS
            elif category == 'distraction':
                distraction_mins += INTERVAL_MINS
                
    total_screen_mins = deep_work_mins + admin_mins + distraction_mins
    
    # Time until break
    # Cap is 2 hours (120 mins) of distraction.
    distraction_cap = 120
    remaining_distraction = max(0, distraction_cap - distraction_mins)
    
    # Percentages
    def calc_pct(part, total):
        return int((part / total * 100)) if total > 0 else 0
        
    stats = {
        "deep_work_mins": int(deep_work_mins),
        "deep_work_pct": calc_pct(deep_work_mins, total_screen_mins),
        "admin_mins": int(admin_mins),
        "admin_pct": calc_pct(admin_mins, total_screen_mins),
        "distraction_mins": int(distraction_mins),
        "distraction_pct": calc_pct(distraction_mins, total_screen_mins),
        "total_screen_mins": int(total_screen_mins),
        "off_pc_mins": int(off_pc_mins),
        "time_until_break_mins": int(remaining_distraction),
        "distraction_cap_mins": distraction_cap
    }

    # Generate Heatmap Data (Multi-day)
    heatmap_data = _generate_heatmap_data(script_path, report_date, range_days)

    colors_data = readjson(os.path.join(script_path, 'web', 'colors.json' ))

    json_data = json.dumps(
        {
            'report_date': report_date_str,
            'generation_date': generation_date,
            'csv_file': csv_file,
            'csv_data': valid_rows, # Only valid user apps for JS visualization
            'heatmap_data': heatmap_data,
            'colors_data': colors_data,
            'stats': stats
        }
    )

    rendered = _render_template(json_data)
    report_filename = os.path.join(script_path, 'web',f'report-{date}.html')
    with open(os.path.join(report_filename), 'w') as f:
        f.write(rendered)

    return report_filename

def _generate_heatmap_data(script_path, current_report_date, range_days):
    """
    Scans for CSV files to build a multi-day activity heatmap.
    Returns a list of dicts: { day: 'MO', day_sort: '2025-10-12', hour: 12, value: 0.0-1.0 }
    """
    import glob
    csv_dir = os.path.join(script_path, 'csv_data')
    files = glob.glob(os.path.join(csv_dir, "watch-*.csv"))
    
    # Parse filenames to Sort
    # watch-MM-DD-YYYY.csv
    date_files = []
    for f in files:
        basename = os.path.basename(f)
        try:
            dstr = basename.replace('watch-', '').replace('.csv', '')
            dObj = datetime.strptime(dstr, '%m-%d-%Y')
            date_files.append((dObj, f))
        except:
            continue
            
    # Sort
    date_files.sort(key=lambda x: x[0])
    
    # Filter to requested range ending at current_report_date
    # Find index of current_report_date or closest previous? 
    # Actually logic: "treat that day as the end of the window".
    
    filtered_files = []
    target_date = current_report_date
    start_date = target_date - timedelta(days=range_days-1)
    
    for dObj, f in date_files:
        # Include if within [start_date, target_date] (inclusive)
        # Compare dates only
        if start_date.date() <= dObj.date() <= target_date.date():
            filtered_files.append((dObj, f))
            
    heatmap_grid = {} # (day_label, hour_int) -> count
    
    max_val = 0

    for dObj, fpath in filtered_files:
        rows = readcsv(fpath)
        for r in rows:
            from activity_classifier import classify_activity
            cat, _ = classify_activity(r)
            if cat in ['off_pc', 'unknown', 'system']: 
                continue
            try:
                ts = datetime.strptime(r['Date'], "%Y-%m-%d %H:%M:%S")
                h = ts.hour
                d_key = dObj.strftime("%Y-%m-%d")
                k = (d_key, h)
                heatmap_grid[k] = heatmap_grid.get(k, 0) + 1
                if heatmap_grid[k] > max_val:
                    max_val = heatmap_grid[k]
            except:
                continue


    # Convert to structured list for JSON
    # We want a sorted list of days.
    # X-axis labels should be day names.
    
    result = []
    
    # Ensure we have entries for all days/hours in the range to complete the grid?
    # Or JS can handle sparse. JS handling sparse is harder. Let's fill zeros.
    
    if not filtered_files:
        return []

    start_date = filtered_files[0][0]
    end_date = filtered_files[-1][0]
    
    delta = end_date - start_date
    
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        d_key = day.strftime("%Y-%m-%d")
        day_label = day.strftime("%a %d") # e.g. Mon 12
        
        for h in range(24):
            val = heatmap_grid.get((d_key, h), 0)
            norm = val / max_val if max_val > 0 else 0
            
            # Thresholding for brightness? Or raw 0-1.
            # Let's pass normalized value.
            result.append({
                "day": day_label, # specific day label
                "day_sort": d_key, # for sorting if needed
                "hour": h,
                "value": norm,
                "raw": val
            })
            
    return result

def _render_template(json_data):
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_loader = FileSystemLoader(os.path.join(script_path, 'web'))
    env = Environment(
        loader=file_loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    
    template = env.get_template('index.html')
    
    return template.render(json_data=json_data)
