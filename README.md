# InfraWatch

InfraWatch is a Python-based infrastructure monitoring and automation tool designed to monitor Linux server health, store historical metrics, expose monitoring data through a REST API, and provide a command-line interface.

Built and tested on AWS EC2 using Python, Linux, SQLite, Docker, Git, and pytest.

## Features

* CPU monitoring
* Memory monitoring
* Disk usage monitoring
* Linux service monitoring
* Overall health evaluation
* Historical metrics using SQLite
* Configurable monitoring thresholds
* Configurable monitoring interval
* REST API
* Command-line interface
* Critical and recovery alerts
* Docker deployment
* Persistent Docker volumes for monitoring data and logs
* Automated health checks
* Pytest test suite

## Architecture

```text
                    INFRAWATCH
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
           CLI/API            Monitoring Loop
              │                   │
              └─────────┬─────────┘
                        ↓
                 Monitoring Engine
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
         CPU          Memory         Disk
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                  Health Engine
                        │
                        ↓
                     SQLite
                        │
                        ↓
                     Alerts
```

## API Endpoints

| Endpoint    | Purpose                               |
| ----------- | ------------------------------------- |
| `/health`   | Current overall health                |
| `/metrics`  | Current CPU, memory, and disk metrics |
| `/services` | Service monitoring status             |
| `/history`  | Historical monitoring data            |
| `/alerts`   | Alert log entries                     |

## CLI

```bash
./infrawatch health
./infrawatch metrics
./infrawatch services
./infrawatch history
```

## Configuration

Configuration is stored in:

```text
config/config.json
```

Example:

```json
{
    "monitoring": {
        "interval": 300,
        "disk_paths": ["/"]
    },
    "thresholds": {
        "warning": 80,
        "critical": 90
    },
    "services": [
        "ssh",
        "cron"
    ],
    "database": {
        "path": "data/infrawatch.db"
    },
    "alerts": {
        "log_file": "logs/alerts.log"
    }
}
```

## Docker

Build the image:

```bash
sudo docker build -t infrawatch .
```

Run InfraWatch:

```bash
sudo docker run -d \
  --name infrawatch \
  -p 5000:5000 \
  --env-file .env \
  -v infrawatch-data:/app/data \
  -v infrawatch-logs:/app/logs \
  infrawatch
```

Check the container:

```bash
sudo docker ps
```

The container includes a Docker health check that verifies the API is responding.

## Persistent Data

Docker volumes are used so monitoring data and logs survive container recreation:

```text
infrawatch-data
infrawatch-logs
```

SQLite database:

```text
data/infrawatch.db
```

Alert log:

```text
logs/alerts.log
```

## Testing

InfraWatch uses pytest.

Run the test suite:

```bash
python -m pytest
```

The project includes tests for health evaluation and system information.

## Security

Secrets such as SMTP credentials are stored in `.env` and excluded from Git using `.gitignore`.

Example:

```text
SMTP_EMAIL=yourgmail@gmail.com
SMTP_PASSWORD=your_app_password
```

The `.env` file should never be committed to GitHub.

## Important Docker Limitation

Linux service monitoring uses `systemctl`, which requires access to the host's systemd environment.

A normal application container does not have access to the host systemd instance. Therefore, `/services` reports:

```text
UNAVAILABLE
Host service monitoring is not available inside Docker
```

This is an intentional architectural limitation rather than an application failure.

Host-level service monitoring can still be performed when InfraWatch runs directly on the Linux host.

## Technology Stack

* Python
* Bash
* Linux
* AWS EC2
* SQLite
* Flask
* Gunicorn
* psutil
* Docker
* pytest
* Git
* GitHub

## Project Structure

```text
infrawatch/
├── config/
│   └── config.json
├── src/
│   └── infrawatch/
│       ├── alerts.py
│       ├── api.py
│       ├── cli.py
│       ├── config.py
│       ├── cpu.py
│       ├── database.py
│       ├── disk.py
│       ├── health.py
│       ├── history.py
│       ├── memory.py
│       ├── monitor.py
│       ├── services.py
│       └── system_info.py
├── tests/
│   ├── test_health.py
│   ├── test_system_info.py
│   └── __init__.py
├── Dockerfile
├── requirements.txt
├── start.sh
└── infrawatch
```

## Project Goal

InfraWatch demonstrates practical DevOps and infrastructure automation concepts including:

* Linux server monitoring
* Python automation
* REST API development
* CLI development
* Configuration management
* Database persistence
* Logging and alerting
* Automated testing
* Docker containerization
* AWS EC2 deployment
* Git and GitHub workflow

