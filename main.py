import subprocess
import sys
import os
from config import COOKIE_VALUE, DEVICE_ID

# Arrays with servers
ntp_servers = [
    "ntp0.ntp-servers.net", "ntp1.ntp-servers.net", "ntp2.ntp-servers.net",
    "ntp3.ntp-servers.net", "ntp4.ntp-servers.net", "ntp5.ntp-servers.net",
    "ntp6.ntp-servers.net"
]

MI_SERVERS = ['sgp-api.buy.mi.com', '20.157.18.26']

# Installing dependencies
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ["requests", "ntplib", "pytz", "urllib3", "icmplib"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing package {package}...")
        install_package(package)

os.system('cls' if os.name == 'nt' else 'clear')

import hashlib
import random
import time
from datetime import datetime, timezone, timedelta
import ntplib
import pytz
import urllib3
import json
import statistics
from icmplib import ping

# Returns average response time
def debug_ping(host):
    try:
        result = ping(host, count=1, interval=0.5, timeout=2)
        return result.avg_rtt if result.is_alive else None
    except Exception as e:
        print(f"Ping error: {e}")
        return None

# Calculates average ping
def get_average_ping():
    all_pings = []
    print("Starting ping calculation...")
    def ping_server(server):
        pings = []
        for attempt in range(3):
            result = debug_ping(server)
            if result is not None:
                pings.append(result)
            time.sleep(0.2)
        return statistics.mean(pings) if pings else None

    for server in MI_SERVERS:
        try:
            ping_time = ping_server(server)
            if ping_time is not None:
                all_pings.append(ping_time)
            else:
                print(f"\nFailed to get ping to server {server}")
        except Exception as e:
            print(f"\nError pinging {server}: {str(e)}")

    if not all_pings:
        print("\nFailed to get ping to any server!")
        print("Using default value: 300 ms")
        return 300
    
    avg_ping = statistics.mean(all_pings)
    print(f"Average ping: {avg_ping:.2f} ms")
    return avg_ping

# Generates unique device identifier
def generate_device_id():
    random_data = f"{random.random()}-{time.time()}"
    device_id = hashlib.sha1(random_data.encode('utf-8')).hexdigest().upper()
    print(f"Generated deviceId: {device_id}")
    return device_id

# Gets current Beijing time via NTP
def get_initial_beijing_time():
    client = ntplib.NTPClient()
    beijing_tz = pytz.timezone("Asia/Shanghai")
    for server in ntp_servers:
        try:
            print(f"Attempting to connect to NTP server: {server}")
            response = client.request(server, version=3)
            ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
            beijing_time = ntp_time.astimezone(beijing_tz)
            print(f"Beijing time received from server {server}: {beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            return beijing_time
        except Exception as e:
            print(f"Failed to connect to {server}: {e}")
    print("Failed to connect to any NTP server.")
    return None

# Synchronizes Beijing time
def get_synchronized_beijing_time(start_beijing_time, start_timestamp):
    elapsed = time.time() - start_timestamp
    current_time = start_beijing_time + timedelta(seconds=elapsed)
    return current_time

# Waits until the specified time considering ping
def wait_until_target_time(start_beijing_time, start_timestamp, ping_delay):
    next_day = start_beijing_time + timedelta(days=1)
    
    network_delay = ping_delay / 2
    server_processing_time = 30
    total_delay = (network_delay - server_processing_time) / 1000.0
    
    target_time = next_day.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=total_delay)
    
    print(f"Waiting until {target_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (Considering approximately calculated network delay).")
    
    while True:
        current_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        time_diff = target_time - current_time
        
        if time_diff.total_seconds() > 1:
            time.sleep(min(1.0, time_diff.total_seconds() - 1))
        elif current_time >= target_time:
            print(f"Time reached: {current_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Starting to send requests...")
            break
        else:
            time.sleep(0.0001)

# Checks the possibility of unlocking the account via API
def check_unlock_status(session, cookie_value, device_id):
    try:
        url = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }
        
        response = session.make_request('GET', url, headers=headers)
        if response is None:
            print("[Error] Failed to get unlock status.")
            return False

        response_data = json.loads(response.data.decode('utf-8'))
        response.release_conn()

        if response_data.get("code") == 100004:
            print("[Error] Cookie expired, needs to be updated!")
            input("Press Enter to close...")
            exit()

        data = response_data.get("data", {})
        is_pass = data.get("is_pass")
        button_state = data.get("button_state")
        deadline_format = data.get("deadline_format", "")

        if is_pass == 4:
            if button_state == 1:
                print("[Status] Account can submit an unlock request.")
                return True
            elif button_state == 2:
                print(f"[Status] Account is blocked from submitting requests until {deadline_format} (Month/Day).")
                input("Press Enter to close...")
                exit()
            elif button_state == 3:
                print("[Status] Account is less than 30 days old.")
                input("Press Enter to close...")
                exit()
        elif is_pass == 1:
            print(f"[Status] Request approved, unlock available until {deadline_format}.")
            input("Press Enter to close...")
            exit()
        else:
            print("[Error] Unknown status.")
            input("Press Enter to close...")
            exit()
    except Exception as e:
        print(f"[Status check error] {e}")
        return False

# Waits until the specified time to start ping calculation
def wait_until_ping_time(start_beijing_time, start_timestamp):
    next_day = start_beijing_time + timedelta(days=0)
    target_time = next_day.replace(hour=23, minute=59, second=30)
    
    print(f"Waiting until {target_time.strftime('%Y-%m-%d %H:%M:%S')} to start ping calculation.")
    
    while True:
        current_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        time_diff = (target_time - current_time).total_seconds()

        if time_diff <= 0:
            print(f"Time reached: {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Starting ping calculation...")
            avg_ping = get_average_ping()
            return avg_ping
        else:
            time.sleep(min(1, time_diff))

# wrapper for working with HTTP requests
class HTTP11Session:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=10,
            retries=True,
            timeout=urllib3.Timeout(connect=1.0, read=4.0),
            headers={}
        )

    def make_request(self, method, url, headers=None, body=None):
        try:
            request_headers = {}
            if headers:
                request_headers.update(headers)
                request_headers['Content-Type'] = 'application/json; charset=utf-8'
            
            if method == 'POST':
                if body is None:
                    body = '{"is_retry":true}'.encode('utf-8')
                request_headers['Content-Length'] = str(len(body))
                request_headers['Accept-Encoding'] = 'gzip, deflate, br'
                request_headers['User-Agent'] = 'okhttp/4.12.0'
                request_headers['Connection'] = 'keep-alive'
            
            response = self.http.request(
                method,
                url,
                headers=request_headers,
                body=body,
                preload_content=False
            )
            
            return response
        except Exception as e:
            print(f"[Network error] {e}")
            return None

def main():
    
    cookie_value = COOKIE_VALUE
    device_id = DEVICE_ID if DEVICE_ID else generate_device_id()
    session = HTTP11Session()

    if check_unlock_status(session, cookie_value, device_id):
        start_beijing_time = get_initial_beijing_time()
        if start_beijing_time is None:
            print("Failed to set initial time. Press Enter to close...")
            input()
            exit()

        start_timestamp = time.time()
        
        avg_ping = wait_until_ping_time(start_beijing_time, start_timestamp)
        
        if avg_ping is None:
            print("Using default ping: 50 ms")
            avg_ping = 50
            
        wait_until_target_time(start_beijing_time, start_timestamp, avg_ping)

        url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }

        try:
            while True:
                request_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(f"\n[Request] Sending request at {request_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")
                
                response = session.make_request('POST', url, headers=headers)
                if response is None:
                    continue

                response_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(f"[Response] Response received at {response_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")

                try:
                    response_data = response.data
                    response.release_conn()
                    json_response = json.loads(response_data.decode('utf-8'))
                    code = json_response.get("code")
                    data = json_response.get("data", {})

                    if code == 0:
                        apply_result = data.get("apply_result")
                        if apply_result == 1:
                            print(f"[Status] Request approved, checking status...")
                            check_unlock_status(session, cookie_value, device_id)
                        elif apply_result == 3:
                            deadline_format = data.get("deadline_format", "Not specified")
                            print(f"[Status] Request not submitted, request limit reached, try again at {deadline_format} (Month/Day).")
                            input("Press Enter to close...")
                            exit()
                        elif apply_result == 4:
                            deadline_format = data.get("deadline_format", "Not specified")
                            print(f"[Status] Request not submitted, blocked from submitting requests until {deadline_format} (Month/Day).")
                            input("Press Enter to close...")
                            exit()
                    elif code == 100001:
                        print(f"[Status] Request rejected, request error.")
                        print(f"[Full server response]: {json_response}")
                    elif code == 100003:
                        print("[Status] Request possibly approved, checking status...")
                        print(f"[Full server response]: {json_response}")
                        check_unlock_status(session, cookie_value, device_id)
                    elif code is not None:
                        print(f"[Status] Unknown request status: {code}")
                        print(f"[Full server response]: {json_response}")
                    else:
                        print("[Error] Response does not contain the required code.")
                        print(f"[Full server response]: {json_response}")

                except json.JSONDecodeError:
                    print("[Error] Failed to decode JSON response.")
                    print(f"Server response: {response_data}")
                except Exception as e:
                    print(f"[Response processing error] {e}")
                    continue

        except Exception as e:
            print(f"[Request error] {e}")
            input("Press Enter to close...")
            exit()

if __name__ == "__main__":
    main()