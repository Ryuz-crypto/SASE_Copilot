mport requests
import json

# Configuration
ORCHESTRATOR_URL = "https://keynote-hpe-discover-orchge-eucentral1.silverpeaksystems.net"
API_KEY = "d506cb83e9f148adb48c12f16f236cc7827bfadfd8be4427b6be100d02d01e1f938ce61f79a545eab1633f1b606b01fd3b4b438c42ff4423afc1f86a9693a4f3"  # Or use session-based authentication

# Headers for API requests
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": API_KEY  # Adjust based on your auth method
}

def get_all_appliances():
    """Retrieve list of all appliances"""
    url = f"{ORCHESTRATOR_URL}/gms/rest/appliance"
    response = requests.get(url, headers=headers, verify=False)
    return response.json()

def get_appliance_alarms(ne_pk):
    """Get alarms for a specific appliance"""
    url = f"{ORCHESTRATOR_URL}/gms/rest/alarm/appliance"
    params = {"nePk": ne_pk}
    response = requests.get(url, headers=headers, params=params, verify=False)
    return response.json()

def collect_all_alarms():
    """Main function to collect alarms from all appliances"""
    all_alarms = []
    
    # Get all appliances
    appliances = get_all_appliances()
    
    for appliance in appliances:
        hostname = appliance.get("hostName", "Unknown")
        ne_pk = appliance.get("nePk")
        
        print(f"Collecting alarms from: {hostname}")
        
        try:
            alarms = get_appliance_alarms(ne_pk)
            for alarm in alarms:
                alarm["applianceName"] = hostname
                all_alarms.append(alarm)
        except Exception as e:
            print(f"Error collecting from {hostname}: {e}")
    
    return all_alarms

if __name__ == "__main__":
    alarms = collect_all_alarms()
    
    # Export to JSON file
    with open("all_alarms.json", "w") as f:
        json.dump(alarms, f, indent=2)
    
    print(f"\nTotal alarms collected: {len(alarms)}")
