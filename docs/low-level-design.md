# Low-Level Design (LLD)
# Python DevOps Time Tracking API

## 1. Document Overview

### 1.1 Purpose

This document provides the detailed technical design for the Python
DevOps Time Tracking API.

The LLD translates the architecture described in the High-Level Design
into concrete application, database, container, networking, security,
monitoring, backup, and deployment specifications.

The implementation is designed for a local/on-premise Docker
environment and does not depend on AWS infrastructure.

---

# 2. System Components

The local deployment consists of the following primary services:

| Service | Purpose | Container |
|---|---|---|
| FastAPI | REST API application | `fastapi_app` |
| MariaDB | Relational database | `devops-mariadb` |
| Prometheus | Metrics collection | `prometheus` |
| Grafana | Monitoring and alerting | `grafana` |

The services communicate through a dedicated Docker network.

---

# 3. Container Specifications

## 3.1 FastAPI Container

| Property | Specification |
|---|---|
| Service name | `web` |
| Container name | `fastapi_app` |
| Application | FastAPI |
| Python version | 3.12 |
| Application server | Uvicorn |
| Internal port | 8000 |
| Host binding | `127.0.0.1:8000` |
| Restart policy | `unless-stopped` |
| Memory limit | 512 MB |
| CPU limit | 1.0 CPU |
| User | Non-root `appuser` |
| Security option | `no-new-privileges:true` |
| Privileged | Disabled |
| Additional capabilities | None |
| Health endpoint | `/health` |

The container starts the database migration process before starting
the Uvicorn application server.

Startup command:

```text
alembic upgrade head
        ↓
uvicorn app.main:app
