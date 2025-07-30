import schedule
import time
from plyer import notification
import datetime

def to_24h(time_str: str) -> str:
    """
    Convert "09:00 AM" or "4:30 PM" → "09:00" or "16:30"
    """
    dt = datetime.datetime.strptime(time_str.strip(), "%I:%M %p")
    return dt.strftime("%H:%M")

def job_notify(description: str):
    notification.notify(
        title="Reminder",
        message=description,
        timeout=5
    )

def schedule_reminders(plan: list):
    """
    plan: list of tuples (start, end, desc)
    Schedules a notification at each start time.
    """
    for start_time, _, desc in plan:
        try:
            hhmm = to_24h(start_time)  # normalize to 24h
            schedule.every().day.at(hhmm).do(job_notify, desc)
        except Exception as e:
            raise ValueError(f"Invalid time format for a daily job ({start_time}): {e}")

    # Run scheduler loop (blocking)
    while True:
        schedule.run_pending()
        time.sleep(1)