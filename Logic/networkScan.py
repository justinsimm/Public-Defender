import subprocess, platform, re
import urllib.request
import json
import socket 

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
    

    return auth, ssid, cipher, wifiIP, DoH, subnet

#Make a domain request throuh encrypted query (Cloudflare)
#Compare data to check for DNS spoofing 
def doh_integrity_check(domain='example.com'):
    # Query via DoH 
    url = f'https://cloudflare-dns.com/dns-query?name={domain}&type=A'
    req = urllib.request.Request(url, headers={'Accept': 'application/dns-json'})

    #Make the query and load the response into a json for comparison
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    #Extract the IPS data from the json received
    doh_ips = {a['data'] for a in data.get('Answer', []) if a['type'] == 1}

    #Make a normal query using unencrypted system
    system_ips = socket.getaddrinfo(domain, None)
    system_ips = {system_ips[0][4][0]}

    if system_ips.issubset(doh_ips):
        return True
    else:
        return False

wifi_available()
