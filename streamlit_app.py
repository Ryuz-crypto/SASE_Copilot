import requests
import json
import urllib3

# Disable SSL warnings (for lab environments only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
APPLIANCE_IP = "https://keynote-hpe-discover-orchge-eucentral1.silverpeaksystems.net"  # Replace with your appliance IP
API_KEY = "d506cb83e9f148adb48c12f16f236cc7827bfadfd8be4427b6be100d02d01e1f938ce61f79a545eab1633f1b606b01fd3b4b438c42ff4423afc1f86a9693a4f3"   # Replace with your API key
BASE_URL = f"https://{APPLIANCE_IP}/rest"

# Headers for authentication
headers = {
    "X-Auth-Token": API_KEY,
    "Content-Type": "application/json"
}

def get_active_flows(filter_type="all", uptime="anytime", protocol=None, application=None):
    """
    Retrieve active flows from the appliance.
    
    Parameters:
    - filter_type: all, asymmetric, passThrough, stale
    - uptime: anytime, last5m, term5m, term
    - protocol: tcp, udp, icmp, etc.
    - application: http, https, cifs_smb, etc.
    """
    endpoint = f"{BASE_URL}/flows"
    
    params = {
        "filter": filter_type,
        "uptime": uptime
    }
    
    if protocol:
        params["protocol"] = protocol
    if application:
        params["application"] = application
    
    try:
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            verify=False  # Set to True in production with valid certs
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving flows: {e}")
        return None

def display_flow_summary(flow_data):
    """Display a summary of the flow data."""
    if not flow_data:
        return
    
    print("\n=== Flow Summary ===")
    print(f"Total Flows: {flow_data.get('total_flows', 0)}")
    print(f"Optimized Flows: {flow_data.get('flows_optimized', 0)}")
    print(f"Passthrough Flows: {flow_data.get('flows_passthrough', 0)}")
    print(f"Management Flows: {flow_data.get('flows_management', 0)}")
    print(f"Returned Flows: {flow_data.get('returned_flows', 0)}")

if __name__ == "__main__":
    # Get all active flows
    flows = get_active_flows()
    
    if flows:
        display_flow_summary(flows)
        
        # Optionally save to file
        with open("active_flows.json", "w") as f:
            json.dump(flows, f, indent=2)
        print("\nFlow data saved to active_flows.json")
