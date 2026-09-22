# High-Level Design (HLD)

# Kimai DevOps Time Tracking Platform

## 1. Document Overview

### 1.1 Purpose

This document describes the high-level architecture of the Kimai DevOps
time-tracking platform.

The system uses the open-source Kimai time-tracking application,
MariaDB for persistent data storage, Docker for containerization,
Terraform for infrastructure provisioning, Prometheus for metrics
collection, and Grafana for monitoring and alerting.

The implementation is deployed locally/on-premise using Docker and
Docker Compose rather than AWS cloud infrastructure.

### 1.2 Design Goals

The primary goals are:

* Provide a functional web-based time-tracking application.
* Store application data reliably in MariaDB.
* Containerize the application and supporting services.
* Provision infrastructure using Terraform.
* Automate build, test, and deployment activities through CI/CD.
* Monitor infrastructure health and resource utilization.
* Provide alerting for high CPU usage, low disk space, and application
  health failures.
* Protect application and database credentials using environment-based
  configuration.
* Provide database backup and restore capability.
* Support Docker image versioning and rollback.
* Keep the environment reproducible and suitable for local/on-premise
  infrastructure.

---

# 2. Architecture Overview

The implemented architecture is:

```text
                         Developer
                            |
                            v
                    Git / GitHub Repository
                            |
                            v
                    GitHub Actions CI/CD
                            |
                            v
                  Docker Image / Versioning
                            |
                +-----------+-----------+
                |                       |
                v                       v
        Docker Compose             Terraform
        Deployment                Infrastructure
                |                       |
                +-----------+-----------+
                            |
                     Docker Network
                            |
       +--------------------+---------------------+
       |                    |                     |
       v                    v                     v
   Kimai App             MariaDB             Monitoring
  kimai_app          devops-mariadb             Stack
       |                    |              +------+------+
       |                    |              |             |
       |                    |              v             v
       |                    |         Prometheus      Grafana
       |                    |              |             |
       |                    |              +-------> Alerts
       |                    |
       +--------------------+
```

---

# 3. Major Components

| Component              | Technology     | Purpose                                  |
| ---------------------- | -------------- | ---------------------------------------- |
| Application            | Kimai          | Time tracking and web application        |
| Database               | MariaDB 11.2.2 | Persistent application storage           |
| Containers             | Docker         | Application and infrastructure isolation |
| Orchestration          | Docker Compose | Local service deployment                 |
| Infrastructure as Code | Terraform      | Reproducible Docker infrastructure       |
| Metrics                | Prometheus     | Metrics collection                       |
| Infrastructure metrics | Node Exporter  | CPU, memory, disk and network metrics    |
| Container metrics      | cAdvisor       | Container-level monitoring               |
| Visualization          | Grafana        | Dashboards and alerting                  |
| Source control         | Git/GitHub     | Version control                          |
| CI/CD                  | GitHub Actions | Automated validation and deployment      |
| Image registry         | Docker Hub     | Versioned container images               |

---

# 4. Networking Architecture

The Docker Compose deployment uses an internal Docker bridge network.

The main services communicate using Docker service/container names rather
than relying on public network access.

Host-facing services are bound to `127.0.0.1` where appropriate.

This prevents the database, monitoring interfaces, and application from
being directly exposed on the host's external network interface.

---

# 5. Security Architecture

The implementation applies the following security controls:

* Database credentials are supplied through environment configuration.
* `.env` is excluded from Git.
* Terraform variable files containing credentials are excluded from Git.
* MariaDB is bound to localhost.
* Kimai is bound to localhost.
* Prometheus and Grafana are bound to localhost.
* Kimai uses Docker `no-new-privileges`.
* Kimai has a Docker health check.
* Containers use restart policies.
* Infrastructure services communicate through a private Docker network.
* Docker image versions are used for infrastructure components.
* Database backup and restore procedures are available.

Cloud-specific controls such as AWS IAM, AWS WAF, Security Groups,
public Application Load Balancers, and bastion hosts are not deployed in
the local implementation. These are documented as cloud architecture
requirements and can be mapped to equivalent controls in a future cloud
deployment.

---

# 6. Monitoring Architecture

Prometheus collects infrastructure metrics from:

* Node Exporter
* cAdvisor

Grafana provides the **Kimai Monitoring** dashboard.

The dashboard includes:

1. CPU Usage
2. Memory Usage
3. Disk Usage
4. Network Receive
5. Network Transmit

Grafana alert rules include:

* Kimai High CPU Usage
* Kimai Low Disk Space
* Kimai Application Health Failure

The alerting system evaluates rules every 10 seconds with a 5-minute
pending period.

---

# 7. Infrastructure as Code

Terraform provisions a local Docker-based infrastructure consisting of:

* Docker network
* MariaDB
* Kimai
* Prometheus
* Grafana

Terraform modules are organized by infrastructure component.

The implementation uses the Docker Terraform provider instead of a cloud
provider because the project is operated locally.

An AWS S3 remote Terraform backend is therefore not implemented.

---

# 8. CI/CD Architecture

The CI/CD workflow is maintained using GitHub Actions.

The pipeline performs automated validation and testing on changes to the
main branch and pull requests.

Docker image versioning is used to support controlled deployment and
rollback.

A Jenkinsfile is maintained as part of the project design for the
requested Jenkins-based CI/CD architecture, but Jenkins itself is not
running in the local implementation.

---

# 9. Backup and Recovery

MariaDB data is stored in persistent Docker volumes.

Database backup and restore procedures are available for recovery testing.

Docker image versioning provides an application rollback mechanism by
allowing a previously tested image version to be deployed.

---

# 10. Cloud Architecture Considerations

The original project requirements reference a multi-cloud architecture
such as AWS and GCP.

The current implementation intentionally uses local/on-premise
infrastructure.

For a future cloud deployment, the logical components can be mapped to:

* Compute → cloud virtual machines or container services
* Database → managed MariaDB-compatible database
* Load balancing → cloud Application Load Balancer
* Firewall → Security Groups / network firewall
* WAF → cloud WAF
* IAM → cloud identity and access management
* Object storage → S3/GCS
* Monitoring → cloud monitoring integrated with Prometheus/Grafana

These cloud resources are design targets and are not claimed as deployed
resources in this implementation.
