# WiFi Pentest Toolkit v1.0

Authorized wireless security testing toolkit for **Kali/Linux** and **rooted Termux** (with compatible USB WiFi adapter).

## Features

| Module | Description |
|--------|-------------|
| Evil Twin AP | Rogue access point with custom SSID |
| Captive Portal | Fake Wi‑Fi login page, credentials logged live to terminal + file |
| Deauth | Disconnect clients from nearby APs |
| Combo | Evil Twin + deauth (best with 2 adapters) |
| Handshake | Capture WPA/WPA2 handshake for offline cracking |
| Cleanup | Restore NetworkManager / stop monitor mode |

## Requirements

- Root privileges
- WiFi adapter with **Monitor Mode + Packet Injection** (and AP mode for Evil Twin)
- Recommended adapters: Alfa AWUS036ACH, TP-Link TL-WN722N v1 (Atheros), etc.
- Termux: rooted device + OTG USB adapter; internal phone WiFi often **cannot** do monitor/AP properly

## Install

### Kali / Debian / Ubuntu

```bash
git clone https://github.com/YOUR_USER/wifi-pentest-toolkit.git
cd wifi-pentest-toolkit
chmod +x installer.sh wifitool.sh modules/*.sh modules/*.py
sudo bash installer.sh
sudo bash wifitool.sh
