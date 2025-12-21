import click
import os
from report_builder import report_builder
from datetime import datetime, timedelta
import webbrowser


def setup_scheduler():
    print("Scheduler setup skipped - running in manual mode")
    return True
@click.command()
@click.option('--daysago', default=0, help="Number of days ago to generate report for (0 for today)")
@click.option('--range', default=7, help="Number of days to include in the heatmap window")
def run(daysago, range):
    """Activity Tracker - Generate desktop activity reports"""
    
    # Setup scheduler and check status
    scheduler_status = setup_scheduler()
    if scheduler_status:
        click.echo(click.style('Background task setup successful', fg='green'))
    else:
        click.echo('Background task already setup or setup skipped')
    
    # Generate report for specified date
    date = datetime.now() - timedelta(days=daysago)
    date_str = date.strftime("%m-%d-%Y")
    report_path = report_builder(date_str, range_days=range)

    if not report_path:
        click.echo(click.style(f'No activity data found for {date_str}', fg='red'))
        return
    
    click.echo(click.style('Report generated successfully', fg='green'))
    click.echo(f'Report saved to: {report_path}')
    
    # Open report in browser
    open_report(report_path)
    
def open_report(report_path):
    """Open report in default web browser"""
    try:
        # Convert to file URL for proper browser opening
        if os.name == 'nt':  # Windows
            report_path = report_path.replace('\\', '/')
        webbrowser.open(f'file://{os.path.abspath(report_path)}')
    except Exception as e:
        click.echo(click.style(f'Error opening report: {e}', fg='yellow'))
        click.echo(f'You can manually open: {report_path}')
    
if __name__ == '__main__':
    run()