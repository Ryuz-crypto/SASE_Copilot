import requests
import json
import time
from datetime import datetime

# Configuration - Update these values
ORCHESTRATOR_URL = "https://your-orchestrator.example.com"
API_KEY = "your-api-key-here"
APPLIANCE_HOSTNAME = "sanjose-01"

# Disable SSL warnings for self-signed certs (remove in production)
requests.packages.urllib3.disable_warnings()

def get_appliance_nepk(session, hostname):
    """Get the appliance nePk from hostname."""
    url = f"{ORCHESTRATOR_URL}/gms/rest/appliance"
    response = session.get(url, verify=False)
    response.raise_for_status()
    
    for appliance in response.json():
        if appliance.get("hostName") == hostname:
            return appliance.get("nePk")
    raise ValueError(f"Appliance '{hostname}' not found")

def get_active_flows(session, nepk, flow_type="0", filter_val="3"):
    """
    Get real-time flow statistics.
    
    flow_type: '0'=TCP accelerated, '1'=TCP unaccelerated, '2'=non-TCP
    filter_val: '3'=all traffic types
    """
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
    # Create session with API key authentication
    session = requests.Session()
    session.headers.update({
        "X-Auth-Token": API_KEY,
        "Content-Type": "application/json"
    })
    
    # Get appliance identifier
    nepk = get_appliance_nepk(session, APPLIANCE_HOSTNAME)
    print(f"Found appliance: {APPLIANCE_HOSTNAME}")
    
    # Collect flow stats for all flow types
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
