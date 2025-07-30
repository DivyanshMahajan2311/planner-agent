from datetime import datetime, timedelta


def generate_schedule(data: dict) -> list:
    """
    Very simple first‑fit scheduler.
    - Start at 6:00 AM
    - Place each task back‑to‑back
    """
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    plan = []

    for task in data.get("tasks", []):
        end_time = start_time + timedelta(minutes=task['duration'])
        plan.append((
            start_time.strftime("%I:%M %p"),
            end_time.strftime("%I:%M %p"),
            task['name']
        ))
        start_time = end_time

    return plan