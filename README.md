# Python DevOps Time Tracking API ⏱️

Hey there! If you've been looking for a rock-solid, production-ready example of how to containerize and deploy a modern web application, you're in the right place.

This is a complete, containerized **FastAPI** time-tracking backend built with production best practices in mind. It goes way beyond just writing code—it handles database migrations, automated testing, CI/CD pipelines, security hardening, monitoring, alerting, and disaster recovery.

---

## 🏗️ Architecture Blueprint

```text
GitHub
  │
  ▼
GitHub Actions (Automated CI/CD Pipeline)
  │
  ▼
Docker Image Registry (Versioned by Commit SHA)
  │
  ▼
Docker Compose Orchestration (Local / Server Deployment)
  ├── FastAPI Application (Non-root, CPU/Memory capped)
  ├── MariaDB (Persistent Storage with automated backups)
  ├── Prometheus (Metrics scraping & monitoring)
  └── Grafana (Dashboards & live email alerting)

```

---

## 🛠️ Technology Stack

* **Core Framework:** Python 3.12, FastAPI, Uvicorn
* **Database & Migrations:** MariaDB, SQLAlchemy, Alembic, PyMySQL
* **Containerization:** Docker, Docker Compose (with health checks & restart policies)
* **Testing & Quality:** Pytest
* **Observability & Ops:** Prometheus, Grafana, GitHub Actions

---

## ✨ Standout Features

### 🚀 Application & API

* High-performance asynchronous REST API built with **FastAPI**.
* Complete **User CRUD lifecycle** with strict request/response validation.
* Seamless **SQLAlchemy ORM** mapping over **MariaDB**.
* Automated database schema synchronization via **Alembic migrations**.

### 🐳 Security & Containerization Hardening

* **Non-Root Execution:** Runs under a dedicated, low-privilege `appuser` account.
* **Privilege Escalation Prevention:** Enforces `no-new-privileges:true` in Docker Compose.
* **Resource Guardrails:** Explicit CPU (`1.0`) and memory (`512m`) limits to prevent runaway resource usage.
* **Smart Health Checks:** Integrated container health probes ensuring services start in the exact dependency order (MariaDB healthy ➔ FastAPI boots).

### 📊 Monitoring, Alerting & Observability

* Built-in Prometheus metrics exposition endpoint (`/metrics`).
* Out-of-the-box **Grafana dashboards** tracking request rates, memory/CPU consumption, and HTTP response statuses.
* Pre-configured **Grafana alerting rules** (Detecting app downtime, 5xx error spikes, or resource saturation) wired to email notifications.

### 🔄 CI/CD & Reliability Engineering

* Fully automated **GitHub Actions pipeline** handling dependency setup, migration checks, pytest suites, and Docker image builds.
* **Traceable Versioning:** Every image build is tagged with both `latest` and its corresponding Git commit SHA.
* **Zero-Downtime Rollover & Rollbacks:** Simple environment-variable driven image switching for instant production rollbacks (`ROLLBACK.md`).
* **Disaster Recovery:** Tested database backup and restoration workflows (`BACKUP_RESTORE.md`).

---

## 🔌 API Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API welcome message |
| `GET` | `/health` | System health check probe |
| `GET` | `/version` | Application version & commit info |
| `GET` | `/metrics` | Prometheus metrics scrape target |
| `GET` | `/users` | Retrieve all users |
| `GET` | `/users/{id}` | Retrieve a specific user by ID |
| `POST` | `/users` | Register a new user |
| `PUT` | `/users/{id}` | Update an existing user record |
| `DELETE` | `/users/{id}` | Delete a user |

---

## ⚙️ Environment Configuration

1. Copy the template file to set up your local configuration:
```bash
cp .env.example .env

```


2. Fill out your `.env` values (make sure to pick strong passwords):
```env
DB_HOST=db
DB_PORT=3306
DB_NAME=devops_db
DB_USER=devuser
DB_PASSWORD=your_secure_database_password

MARIADB_ROOT_PASSWORD=your_secure_root_password

DOCKERHUB_USERNAME=your_dockerhub_username
IMAGE_TAG=latest

```



> ⚠️ **Security Note:** Never commit your actual `.env` file or SQL dumps to version control. They are blocked by default via `.gitignore`.

---

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/sxnthosh-dev/python-devops-project.git
cd python-devops-project

```

### 2. Set up a local Python virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Start the application stack with Docker Compose

```bash
docker compose up -d

```

### 5. Verify running services

```bash
docker compose ps

```

### 6. Perform a quick health check

```bash
curl http://localhost:8000/health

```

*Expected response:*

```json
{"status":"healthy"}

```

---

## 🌐 Application & Monitoring URLs

Once running, you can access the various services locally:

| Service | Local URL |
| --- | --- |
| **FastAPI REST API** | [http://localhost:8000](http://localhost:8000?utm_source=gemini) |
| **Interactive Swagger Docs** | [http://localhost:8000/docs](http://localhost:8000/docs?utm_source=gemini) |
| **Prometheus Dashboard** | [http://localhost:9090](http://localhost:9090?utm_source=gemini) |
| **Grafana UI** | [http://localhost:3000](http://localhost:3000?utm_source=gemini) |

---

## 🗄️ Database Migrations (Alembic)

The application automatically runs pending migrations on startup, but you can also manage them manually:

* **Generate a new migration:**
```bash
docker compose exec web alembic revision --autogenerate -m "describe your changes"

```


* **Apply migrations to the database:**
```bash
docker compose exec web alembic upgrade head

```


* **Check current active revision:**
```bash
docker compose exec web alembic current

```



---

## 🧪 Running Automated Tests

The application uses `pytest` to test validation rules, route logic, and DB integration:

* **Run all tests:**
```bash
pytest

```


* **Run tests with verbose breakdown:**
```bash
pytest -v

```



---

## 📦 Backup & Disaster Recovery

* **Create a database backup snapshot:**
```bash
docker compose exec db mariadb-dump -udevuser -p"$DB_PASSWORD" devops_db > backup.sql

```


* For step-by-step restoration and verification instructions, check [BACKUP_RESTORE.md](https://www.google.com/search?q=BACKUP_RESTORE.md&utm_source=gemini).

---

## 🔄 Rolling Back Deployments

Because images are tracked using commit hashes, rolling back to a stable previous version is straightforward:

```bash
export IMAGE_TAG=<previous-stable-commit-sha>
docker compose pull
docker compose up -d

```

*Detailed recovery steps are available in [ROLLBACK.md](ROLLBACK.md).*

---

## 📁 Project Tree Structure

```text
python-devops-project/
├── app/
│   ├── api/          # API routers (e.g., users.py)
│   ├── core/         # Configuration & app settings
│   ├── crud/         # Database operations logic
│   ├── db/           # SQLAlchemy models & session setups
│   ├── schemas/      # Pydantic validation schemas
│   ├── main.py       # FastAPI application entrypoint
│   └── logging_config.py
├── alembic/          # Database migration scripts & env config
├── prometheus/       # Prometheus scraper configs
├── grafana/          # Dashboard definitions & alerts
├── tests/            # Pytest test suite
├── .github/workflows/# GitHub Actions CI/CD pipelines
├── Dockerfile        # Multi-stage production container build
├── docker-compose.yml# Multi-container local orchestration
├── requirements.txt  # Python package dependencies
├── BACKUP_RESTORE.md # Disaster recovery documentation
├── ROLLBACK.md       # Rollback execution runbook
└── README.md

```

---

## 📜 License

Distributed under the **MIT License**. Created for portfolio demonstration, learning, and enterprise deployment patterns.