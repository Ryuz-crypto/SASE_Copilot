import os
import sys
import time
import requests
from urllib3.exceptions import InsecureRequestWarning

# Si en desarrollo necesitas desactivar warnings (NO recomendado en producción)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "https://keynote-hpe-discover-orchge-eucentral1.silverpeaksystems.net")
API_KEY = os.getenv("ORCHESTRATOR_API_KEY","d506cb83e9f148adb48c12f16f236cc7827bfadfd8be4427b6be100d02d01e1f938ce61f79a545eab1633f1b606b01fd3b4b438c42ff4423afc1f86a9693a4f3")  # poner la API en la variable de entorno

if not API_KEY:
    print("ERROR: Debes establecer la variable de entorno ORCHESTRATOR_API_KEY con tu clave de API.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": API_KEY,
}

# Configuración: en producción usar verify=True
VERIFY_TLS = False
TIMEOUT = 10  # segundos


def _fetch_json(session, url):
    resp = session.get(url, headers=HEADERS, verify=VERIFY_TLS, timeout=TIMEOUT)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        raise RuntimeError(f"Respuesta no es JSON desde {url}: {resp.text[:200]}")


def _iter_alarms(data):
    # Acepta tanto listas como objetos con key 'items'/'alarms'
    if isinstance(data, list):
        yield from data
    elif isinstance(data, dict):
        for key in ("items", "alarms", "data"):
            if key in data and isinstance(data[key], list):
                yield from data[key]
                return
        # fallback: intentar iterar sobre una lista bajo otra clave
        # si no hay listas, devolver el dict como único elemento
        yield data
    else:
        yield data


def format_appliance_alarm(a):
    return {
        "host": a.get("hostName", "N/A"),
        "severity": a.get("severity", "N/A"),
        "description": a.get("description", "N/A"),
        "time": a.get("alarmTime", "N/A"),
        "recommended_action": a.get("recommendedAction", "N/A"),
    }


def format_orch_alarm(a):
    return {
        "source": a.get("source", "N/A"),
        "severity": a.get("severity", "N/A"),
        "description": a.get("description", "N/A"),
        "time": a.get("alarmTime", "N/A"),
    }


def get_all_alarms():
    appliance_url = f"{ORCHESTRATOR_URL.rstrip('/')}/gms/rest/alarm/appliance"
    orch_url = f"{ORCHESTRATOR_URL.rstrip('/')}/gms/rest/alarm/gms"

    session = requests.Session()

    try:
        print("=" * 60)
        print("APPLIANCE ALARMS")
        print("=" * 60)
        appliance_data = _fetch_json(session, appliance_url)
        for alarm in _iter_alarms(appliance_data):
            fa = format_appliance_alarm(alarm)
            print(f"Host: {fa['host']}")
            print(f"Severity: {fa['severity']}")
            print(f"Description: {fa['description']}")
            print(f"Time: {fa['time']}")
            print(f"Recommended Action: {fa['recommended_action']}")
            print("-" * 40)

        print("\n" + "=" * 60)
        print("ORCHESTRATOR ALARMS")
        print("=" * 60)
        orch_data = _fetch_json(session, orch_url)
        for alarm in _iter_alarms(orch_data):
            fo = format_orch_alarm(alarm)
            print(f"Source: {fo['source']}")
            print(f"Severity: {fo['severity']}")
            print(f"Description: {fo['description']}")
            print(f"Time: {fo['time']}")
            print("-" * 40)

    except requests.exceptions.RequestException as e:
        print(f"Error de red al obtener alarmas: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error procesando datos: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    get_all_alarms()
