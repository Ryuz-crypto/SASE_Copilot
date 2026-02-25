import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings (for lab environments only)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration - Update these values
ORCHESTRATOR_URL = "URL"
API_KEY = "API_AQUI"  # Or use username/password authentication

def get_all_alarms():
    """Collect alarms from all appliances and Orchestrator"""
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": API_KEY
    }
    
    # Get appliance alarms
    appliance_alarms_url = f"{ORCHESTRATOR_URL}/gms/rest/alarm/appliance"
    
    # Get Orchestrator alarms
    orchestrator_alarms_url = f"{ORCHESTRATOR_URL}/gms/rest/alarm/gms"
    
    try:
        # Fetch appliance alarms
        print("=" * 60)
        print("APPLIANCE ALARMS")
        print("=" * 60)
        
        response = requests.get(appliance_alarms_url, headers=headers, verify=False)
        response.raise_for_status()
        appliance_alarms = response.json()
        
        for alarm in appliance_alarms:
            print(f"Host: {alarm.get('hostName', 'N/A')}")
            print(f"Severity: {alarm.get('severity', 'N/A')}")
            print(f"Description: {alarm.get('description', 'N/A')}")
            print(f"Time: {alarm.get('alarmTime', 'N/A')}")
            print(f"Recommended Action: {alarm.get('recommendedAction', 'N/A')}")
            print("-" * 40)
        
        # Fetch Orchestrator alarms
        print("\n" + "=" * 60)
        print("ORCHESTRATOR ALARMS")
        print("=" * 60)
        
        response = requests.get(orchestrator_alarms_url, headers=headers, verify=False)
        response.raise_for_status()
        orch_alarms = response.json()
        
        for alarm in orch_alarms:
            print(f"Source: {alarm.get('source', 'N/A')}")
            print(f"Severity: {alarm.get('severity', 'N/A')}")
            print(f"Description: {alarm.get('description', 'N/A')}")
            print(f"Time: {alarm.get('alarmTime', 'N/A')}")
            print("-" * 40)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching alarms: {e}")

if __name__ == "__main__":
    get_all_alarms()
