# High-Level Design (HLD)
# Python DevOps Time Tracking API

## 1. Document Overview

### 1.1 Purpose

This document describes the high-level architecture and design of the
Python DevOps Time Tracking API.

The project is a containerized FastAPI application backed by MariaDB.
It includes database migrations, automated testing, CI/CD automation,
monitoring, alerting, logging, security hardening, backup and rollback
capabilities.

The infrastructure is designed and operated locally using Docker and
Docker Compose rather than relying on AWS cloud infrastructure.

### 1.2 Design Goals

The primary goals of the system are:

- Provide a REST API for time-tracking/user-related operations.
- Store application data in MariaDB.
- Provide reliable database schema management using Alembic.
- Containerize the application and supporting infrastructure.
- Automate testing and deployment through CI/CD.
- Monitor application and infrastructure metrics.
- Provide operational alerting.
- Protect application secrets and containers.
- Provide database backup and restore capability.
- Support versioned Docker images and deployment rollback.
- Keep the architecture simple, reproducible, and suitable for local
  infrastructure.

---

# 2. Architecture Overview

The system consists of the following major components:

```text
                         Developer
                            |
                            v
                     Git / GitHub
                            |
                            v
                    CI/CD Automation
                            |
                            v
                     Docker Image
                            |
                            v
                    Docker Compose
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
     FastAPI API         MariaDB          Monitoring
     Container           Database         Infrastructure
          |                                  |
          |                            +-----+------+
          |                            |            |
          |                            v            v
          |                       Prometheus     Grafana
          |                            |            |
          |                            +------> Alerts
          |
          +--------------------> Application Logs
