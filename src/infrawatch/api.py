from flask import Flask, jsonify

from .health import get_current_health
from .database import create_database

app = Flask(__name__)

create_database()

@app.route("/health", methods=['GET'])
def health():
    status = get_current_health()

    return jsonify(
            {
                "status": status
            }
        )

@app.route("/metrics", methods=["GET"])
def metrics():
    from .cpu import get_cpu_info
    from .memory import get_memory_info
    from .disk import get_disk_info
    from .services import monitor_services

    cpu_usage, cpu_cores, load_average = get_cpu_info()
    _, _, _, memory_percentage = get_memory_info()
    root_disk = get_disk_info("/")

    services = []
    service_results = monitor_services(services)

    return jsonify({
        "cpu": cpu_usage,
        "memory": memory_percentage,
        "disk": root_disk["percentage"]
    })

@app.route("/services", methods=["GET"])
def services():
    return jsonify({
        "status": "UNAVAILABLE",
        "reason": "Host service monitoring is not available inside Docker"
    })

@app.route("/history", methods=["GET"])
def history():
    from .database import get_recent_metrics

    rows = get_recent_metrics(10)

    results = []

    for row  in rows:
        results.append({
            "timestamp": row[0],
            "cpu": row[1],
            "memory": row[2],
            "disk": row[3],
            "status": row[4]
        })

    return jsonify(results)

@app.route("/alerts", methods=["GET"])
def alerts():
    log_file = "logs/alerts.log"

    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return jsonify([])

    results = []

    for line in lines:
        line = line.strip()

        if line:
            results.append(line)

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
