import os
import openai
from dotenv import load_dotenv
from tools.parser import parse_input
from tools.scheduler import generate_schedule
from tools.reminders import schedule_reminders
from tools.blocker import block_sites, unblock_sites

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    user_text = input("Paste your tasks, meetings, habits, goals:\n")
    data = parse_input(user_text)
    plan = generate_schedule(data)

    print("\nYour Daily Plan:\n")
    for start, end, desc in plan:
        print(f"{start} – {end}: {desc}")

    # Optional: schedule reminders
    schedule_reminders(plan)

    # Optional: block distracting sites during focus sessions
    block_sites(data.get("block_list", []))


if __name__ == "__main__":
    main()