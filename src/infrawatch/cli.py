import urllib.request
import json
import sys

def get_api_data(url):
    response = urllib.request.urlopen(url)

    data = response.read()

    result = json.loads(data)

    return result

def get_health():
    url = "http://127.0.0.1:5000/health"
    return get_api_data(url)

def get_metrics():
    url = "http://127.0.0.1:5000/metrics"
    return get_api_data(url)


def get_services():
    url = "http://127.0.0.1:5000/services"
    return get_api_data(url)


def get_history():
    url = "http://127.0.0.1:5000/history"
    return get_api_data(url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./infrawatch <command>")
        print("Commands: health, metrics, services, history")
        sys.exit(1)

    command = sys.argv[1]

    if command == "health":
        result = get_health()

        print("InfraWatch Health")
        print("-----------------")
        print("Status:", result["status"])

    elif command == "metrics":
        result = get_metrics()
        print("InfraWatch Metrics")
        print("------------------")
        print("CPU:", result["cpu"], "%")
        print("Memory:", result["memory"], "%")
        print("Disk:", result["disk"], "%")

        print("\nServices")
        print("--------")

        for service, status in result["services"].items():
            print(service, status)

    elif command == "services":
        result = get_services()
        
        print("InfraWatch Services")
        print("-------------------")

        for service, status in result.items():
            print(f"{service}: {status}")

    elif command == "history":
        result = get_history()
        
        print("InfraWatch History")
        print("------------------")

        for row in result:
            print(
                row["timestamp"],
                "CPU:", row["cpu"], "%",
                "Memory:", row["memory"], "%",
                "Disk:", row["disk"], "%"
        )

    else:
        print("Unknown command:", command)
        sys.exit(1)
