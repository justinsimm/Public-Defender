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

    print(output)

    #Obtain fields from the output
    auth = re.search(r'Authentication\s+:\s+(.+)', output)
    if auth:
        auth = auth.group(1).strip()

    ssid = re.search(r'SSID\s+:\s+(.+)', output)
    if ssid:
        ssid = ssid.group(1).strip()

    cipher = re.search(r'Cipher\s+:\s+(.+)', output)
    if cipher:
        cipher = cipher.group(1).strip()

    vpn = re.search(r'VPN\s+:\s+(.+)', output)
    if vpn:
        vpn = vpn.group(1).strip()

    wps = re.search(r'WPS\s+:\s+(.+)', output)
    if wps:
        wps = wps.group(1).strip()
    
    

wifi_available()
