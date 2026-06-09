"""
Daily News Email Scheduler
Runs news_email.py every day at 9:00 AM
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime

def send_news_email():
    """Run the news email script"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled news email task...")
    
    try:
        # Run the news_email.py script
        result = subprocess.run([sys.executable, 'news_email.py'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running news_email.py: {e}")
        print(e.output)
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """Main scheduler function"""
    print("=" * 50)
    print("Daily News Email Scheduler")
    print("=" * 50)
    print("Starting scheduler...")
    print("Email will be sent daily at 9:00 AM")
    print("Press Ctrl+C to stop the scheduler")
    print("=" * 50)
    
    # Schedule the job every day at 9:00 AM
    schedule.every().day.at("09:00").do(send_news_email)
    
    # Run immediately on startup (for testing)
    print("\nRunning initial email send (testing)...")
    send_news_email()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()