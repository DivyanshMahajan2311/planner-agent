import re

def parse_input(text: str) -> dict:
    """
    Parse lines like:
      "Write report (2h)", "Meeting at 11:00 (1h)", "Meditation (30m)"
    Returns a dict with:
      tasks: list of {name, duration_minutes, type}
      block_list: optional list of URLs to block
    """
    tasks = []
    block_list = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Check for a block list section
        if line.lower().startswith("block:"):
            urls = re.findall(r"https?://\S+", line)
            block_list.extend(urls)
            continue

        # Extract duration
        m = re.search(r"\((\d+)(h|m)\)", line)
        if m:
            amount, unit = m.groups()
            minutes = int(amount) * (60 if unit == 'h' else 1)
        else:
            minutes = 30  # default

        # Separate name from parens
        name = re.sub(r"\(.*\)", "", line).strip()
        tasks.append({"name": name, "duration": minutes})

    return {"tasks": tasks, "block_list": block_list}