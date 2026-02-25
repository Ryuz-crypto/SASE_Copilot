import requests
import json
import time
from datetime import datetime


ORCHESTRATOR_URL = "https://keynote-hpe-discover-orchge-eucentral1.silverpeaksystems.net"
API_KEY = "d506cb83e9f148adb48c12f16f236cc7827bfadfd8be4427b6be100d02d01e1f938ce61f79a545eab1633f1b606b01fd3b4b438c42ff4423afc1f86a9693a4f3"
APPLIANCE_HOSTNAME = "4.NE"

requests.packages.urllib3.disable_warnings()

def get_appliance_nepk(session, hostname):
    url = f"{ORCHESTRATOR_URL}/gms/rest/appliance"
    response = session.get(url, verify=False)
    response.raise_for_status()
    
    for appliance in response.json():
        if appliance.get("hostName") == hostname:
            return appliance.get("nePk")
    raise ValueError(f"Appliance '{hostname}' not found")

def get_active_flows(session, nepk, flow_type="0", filter_val="3"):
    url = f"{ORCHESTRATOR_URL}/gms/rest/realtimeStats"
    params = {"nePk": nepk}
    payload = {
        "type": "flow",
        "name": flow_type,
        "filter": filter_val
    }
    
    response = session.post(url, params=params, json=payload, verify=False)
    response.raise_for_status()
    return response.json()

def main():
    session = requests.Session()
    session.headers.update({
        "X-Auth-Token": API_KEY,
        "Content-Type": "application/json"
    })    
    nepk = get_appliance_nepk(session, APPLIANCE_HOSTNAME)
    print(f"Found appliance: {APPLIANCE_HOSTNAME}")
    flow_types = {
        "0": "TCP Accelerated",
        "1": "TCP Unaccelerated", 
        "2": "Non-TCP/UDP"
    }
    
    print(f"\n=== Active Flows Report - {datetime.now()} ===\n")
    
    total_existing = 0
    for ftype, description in flow_types.items():
        stats = get_active_flows(session, nepk, flow_type=ftype)
        
        # Extract EXISTING (active) flow count
        if "EXISTING" in stats and stats["EXISTING"]:
            existing = stats["EXISTING"][-1][1]  # Latest value
            total_existing += existing
            print(f"{description}: {existing:,} active flows")
    
    print(f"\nTotal Active Flows: {total_existing:,}")
if __name__ == "__main__":
    main()
