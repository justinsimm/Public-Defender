# Public-Defender
Wireless networks in public spaces can often be prone to privacy and security risks. An application focused on analyzing these networks and user’s device configurations could provide users early warnings of potential hazards, ultimately providing users with a more secure connection to public networks.

## Requires:
Windows
Admin access
customtkinter
cryptography

## Install
```Bash 
pip install customtkinter
pip install cryptography
```

## Run
```Bash
cd UI
python main.py
```

## Learning Goals Hit
### SLO1 - Basic Network Threats
The application itself focues on the basic of network security and how to avoid basic threats such as that come from having an unencrypted dns, weak authorization, and cipher.

### SLO3 - Access Control Mechanisms
The application requires the user to have admin privlidges. This is a weak access control since admin privledges are often targets for attack.

### SLO4 - Basic Cryptographic Operations
This application implements encryption of it's history using fernet a common python encryption. In a realistic environment the key would need to be kept in a more secure environment but for now is kept in /Demo after running a scan.

### SLO5 - Privacry Threats
The DoH check makes sure DoH is turned on and makes DNS traffic look like standard HTTPS traffic.The DoH integrity checks that system socket calls are receiving the same info as the cloudflare DNS. Ensuring that packets are not being spoofed.
