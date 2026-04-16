import subprocess, platform, re

def wifi_available():
    # Check for matching os
    if platform.system() != 'Windows':
        return False
    
    # Capture basic network info
    result = subprocess.run(
        ['netsh', 'wlan', 'show', 'interfaces'],
        capture_output=True, text=True
    )
    output = result.stdout

    #Return if no wireles network is found
    if (output == "There is no wireless interface on the system."):
        return False

    # Extract any field with a regex like this:
    auth = re.search(r'Authentication\s+:\s+(.+)', output)
    if auth:
        print(auth.group(1).strip())

wifi_available()
