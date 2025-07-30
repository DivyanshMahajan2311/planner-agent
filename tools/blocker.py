import os
import platform

SYSTEM = platform.system()
if SYSTEM == 'Windows':
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_PATH = "/etc/hosts"
REDIRECT = "127.0.0.1"

def block_sites(urls: list):
    """
    Add entries to the hosts file to redirect given domains to localhost.
    """
    if not os.path.exists(HOSTS_PATH):
        raise FileNotFoundError(f"Hosts file not found at {HOSTS_PATH}")

    # Read existing entries
    with open(HOSTS_PATH, 'r') as f:
        lines = f.readlines()

    # Prepare new entries
    entries = []
    for url in urls:
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        entry = f"{REDIRECT} {domain}\n"
        if entry not in lines:
            entries.append(entry)

    # Write entries if any (requires admin privileges)
    if entries:
        with open(HOSTS_PATH, 'a') as f:
            f.writelines(entries)

def unblock_sites(urls: list):
    """
    Remove entries for given domains from the hosts file.
    """
    if not os.path.exists(HOSTS_PATH):
        raise FileNotFoundError(f"Hosts file not found at {HOSTS_PATH}")

    with open(HOSTS_PATH, 'r') as f:
        lines = f.readlines()

    with open(HOSTS_PATH, 'w') as f:
        for line in lines:
            if not any(
                url.replace('https://', '').replace('http://', '').split('/')[0] in line
                for url in urls
            ):
                f.write(line)
