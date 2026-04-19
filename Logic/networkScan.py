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
    if result.returncode != 0 or not output.strip():
        return False

    print(output)

    #Get Authentication method
    auth = re.search(r'Authentication\s+:\s+(.+)', output)
    if auth:
        auth = auth.group(1).strip()

    #Get network name
    ssid = re.search(r'SSID\s+:\s+(.+)', output)
    if ssid:
        ssid = ssid.group(1).strip()

    #Get cypher type
    cipher = re.search(r'Cipher\s+:\s+(.+)', output)
    if cipher:
        cipher = cipher.group(1).strip()

    # Capture advanced network info
    result = subprocess.run(
        ['ipconfig', '/all'],
        capture_output=True, text=True
    )
    output = result.stdout
    

    #DoH check
    #DoH prevents unencrypted queries
    DoH = re.search(r'DoH:\s+(.+)', output)
    if DoH:
        DoH = DoH.group(1).strip()

    blocks = re.split(r'\r?\n\r?\n', output)

    for block in blocks:
        if 'Wi-Fi' in block or 'Wireless' in block:
            wifiIP = re.search(r'IPv4 Address[. ]+:\s*([\d.]+)', block)
            if wifiIP:
                wifiIP = wifiIP.group(1).strip()
            subnet = re.search(r'Subnet Mask[\s.]+:\s*([\d.]+)', block)
            #Check for large subnetwork (increased security risk)
            if subnet:
                subnet = subnet.group(1).strip()
    

    return auth, ssid, cipher, wifiIP, DoH

    

wifi_available()
