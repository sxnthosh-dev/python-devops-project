# Low-Level Design (LLD)

# Kimai DevOps Time Tracking Platform

## 1. Document Overview

This document provides the detailed technical design of the implemented Kimai DevOps platform.

The system is deployed locally using Docker, Docker Compose, and Terraform. Monitoring is provided by Prometheus, Node Exporter, cAdvisor, and Grafana. CI/CD is implemented using GitHub Actions, with a Jenkinsfile maintained for the original project requirement.

Cloud-specific requirements that are not deployed in the local environment are documented separately under the Cloud Requirement Mapping section.

---

# 2. Service Architecture

| Service       | Image                              | Container        | Host Port | Container Port |
| ------------- | ---------------------------------- | ---------------- | --------: | -------------: |
| Kimai         | `sxnthosh/kimai-devops:1.0.0`      | `kimai_app`      |      8000 |           8001 |
| MariaDB       | `mariadb:11.2.2`                   | `devops-mariadb` |      3307 |           3306 |
| Prometheus    | `prom/prometheus:v2.51.0`          | `prometheus`     |      9090 |           9090 |
| Grafana       | `grafana/grafana:10.4.0`           | `grafana`        |      3000 |           3000 |
| Node Exporter | `prom/node-exporter:v1.8.1`        | `node-exporter`  |  Internal |           9100 |
| cAdvisor      | `gcr.io/cadvisor/cadvisor:v0.49.1` | `cadvisor`       |      8080 |           8080 |

The Docker Compose services communicate through the `internal-network` Docker bridge network.

Host-accessible services are bound to `127.0.0.1` to prevent direct external access in the local deployment.

---

# 3. Kimai Application

## 3.1 Container Configuration

| Property        | Value                         |
| --------------- | ----------------------------- |
| Image           | `sxnthosh/kimai-devops:1.0.0` |
| Container       | `kimai_app`                   |
| Internal port   | 8001                          |
| Host binding    | `127.0.0.1:8000`              |
| Restart policy  | `unless-stopped`              |
| Health check    | Enabled                       |
| Security option | `no-new-privileges:true`      |

The custom Kimai image is based on the official Kimai image:

```dockerfile
FROM kimai/kimai2:stable
```

The project Dockerfile adds the required application port and container health check.

The health check verifies the Kimai HTTP service:

```text
curl -f http://127.0.0.1:8001
```

The container has been verified as healthy and the application responds with HTTP `302 Found`, redirecting to the Kimai homepage.

The official Kimai image's default user configuration is retained rather than forcing a custom user override that could interfere with the image entrypoint or filesystem permissions.

---

# 4. MariaDB

## 4.1 Database Configuration

| Property           | Value            |
| ------------------ | ---------------- |
| Image              | `mariadb:11.2.2` |
| Container          | `devops-mariadb` |
| Internal port      | 3306             |
| Host binding       | `127.0.0.1:3307` |
| Database           | Kimai database   |
| Restart policy     | `unless-stopped` |
| Persistent storage | Docker volume    |
| Health check       | Enabled          |

Kimai connects to MariaDB through the Docker service name:

```text
db:3306
```

The database uses persistent Docker storage.

The MariaDB host port is bound to localhost and is therefore not directly exposed on the external network interface.

The project also retains the existing `devops_db` database used by the earlier FastAPI stage. The current Kimai deployment uses the separate `kimai` database.

---

# 5. Docker Network

The Compose deployment uses:

```text
internal-network
```

Network type:

```text
bridge
```

Application, database, and monitoring services communicate through this private Docker network.

The main service communication path is:

```text
Kimai
  |
  | db:3306
  v
MariaDB
```

Monitoring communication is:

```text
Prometheus
   |
   +---- node-exporter:9100
   |
   +---- cadvisor:8080
```

Grafana uses Prometheus as its monitoring data source.

Host port bindings use `127.0.0.1` for services that require access from the local machine.

---

# 6. Monitoring

## 6.1 Prometheus

Prometheus runs on:

```text
127.0.0.1:9090
```

The active Compose Prometheus configuration scrapes:

```yaml
scrape_configs:
  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "cadvisor"
    static_configs:
      - targets: ["cadvisor:8080"]
```

Both configured Prometheus targets have been verified as healthy.

---

## 6.2 Node Exporter

Node Exporter exposes host infrastructure metrics on:

```text
node-exporter:9100
```

Metrics include:

* CPU utilization
* Memory utilization
* Filesystem usage
* Network traffic

These metrics are used by Grafana for infrastructure monitoring and alerting.

---

## 6.3 cAdvisor

cAdvisor exposes container metrics on:

```text
cadvisor:8080
```

cAdvisor provides container-level monitoring information to Prometheus.

The Kimai application health alert uses container monitoring information to detect when the expected Kimai application container is no longer being reported.

---

# 7. Grafana

Grafana runs on:

```text
127.0.0.1:3000
```

Prometheus is configured as the Grafana data source.

The primary dashboard is:

```text
Kimai Monitoring
```

The dashboard contains the following infrastructure panels.

## Panel 1 — CPU Usage

```promql
100 - (
  avg by(instance) (
    rate(node_cpu_seconds_total{job="node",mode="idle"}[5m])
  ) * 100
)
```

This calculates CPU utilization from the idle CPU percentage.

---

## Panel 2 — Memory Usage

```promql
(
  1 -
  (
    node_memory_MemAvailable_bytes{job="node"}
    /
    node_memory_MemTotal_bytes{job="node"}
  )
) * 100
```

This calculates percentage memory utilization.

---

## Panel 3 — Disk Usage

```promql
100 * (
  1 -
  (
    node_filesystem_avail_bytes{job="node"}
    /
    node_filesystem_size_bytes{job="node"}
  )
)
```

This calculates filesystem utilization.

---

## Panel 4 — Network Receive

```promql
sum by(device) (
  rate(node_network_receive_bytes_total{job="node"}[5m])
)
```

This displays incoming network traffic.

---

## Panel 5 — Network Transmit

```promql
sum by(device) (
  rate(node_network_transmit_bytes_total{job="node"}[5m])
)
```

This displays outgoing network traffic.

---

# 8. Grafana Alert Rules

Three Grafana alert rules are configured.

## 8.1 Kimai High CPU Usage

Query:

```promql
100 * (
  1 -
  avg(
    rate(node_cpu_seconds_total{
      job="node",
      mode="idle"
    }[5m])
  )
)
```

Condition:

```text
Above 80
```

Pending period:

```text
5 minutes
```

Evaluation interval:

```text
10 seconds
```

The alert is intended to identify sustained high host CPU utilization.

---

## 8.2 Kimai Low Disk Space

Query:

```promql
100 * (
  node_filesystem_avail_bytes{
    job="node",
    fstype!="",
    mountpoint!~"/proc.*|/sys.*|/dev.*"
  }
  /
  node_filesystem_size_bytes{
    job="node",
    fstype!="",
    mountpoint!~"/proc.*|/sys.*|/dev.*"
  }
)
```

Condition:

```text
Below 20
```

Pending period:

```text
5 minutes
```

Evaluation interval:

```text
10 seconds
```

The rule monitors available filesystem capacity and alerts when available space remains below the configured threshold.

---

## 8.3 Kimai Application Health Failure

The application health rule monitors the expected Kimai application container through cAdvisor metrics.

The alert is triggered when the expected Kimai container monitoring information is no longer available.

Pending period:

```text
5 minutes
```

Evaluation interval:

```text
10 seconds
```

The alert is currently configured and has been verified in the Normal state.

---

# 9. Terraform Infrastructure

Terraform uses the Docker provider to provision local infrastructure.

The Terraform implementation includes resources for:

* Docker network
* MariaDB
* Kimai
* Prometheus
* Grafana

The root Terraform configuration retains the existing module name `fastapi` for state/module compatibility, while the deployed application resource has been migrated to Kimai.

The application resources are now named and configured for Kimai.

The Terraform-managed Kimai container is:

```text
terraform-kimai-app
```

The Terraform-managed services use separate host ports from the Docker Compose stack.

| Service    | Terraform Host Port | Container Port |
| ---------- | ------------------: | -------------: |
| Kimai      |                8002 |           8001 |
| MariaDB    |                3308 |           3306 |
| Prometheus |                9091 |           9090 |
| Grafana    |                3001 |           3000 |

Terraform and Docker Compose therefore provide separate local infrastructure instances and avoid host-port conflicts.

### Terraform Outputs

The Terraform configuration provides outputs for:

```text
kimai_url
kimai_health_url
prometheus_url
grafana_url
mariadb_host
docker_network
```

Example local endpoints:

```text
Kimai:      http://127.0.0.1:8002
Prometheus: http://127.0.0.1:9091
Grafana:    http://127.0.0.1:3001
```

---

# 10. Terraform Security

Terraform variables containing credentials are marked sensitive where appropriate.

Local Terraform variable files are excluded from Git:

```text
terraform/*.tfvars
```

The `.env` file is also excluded from Git.

Only example configuration files intended for version control are tracked.

Terraform state is currently stored locally because this implementation does not use an AWS S3 remote backend.

---

# 11. Container Security

The Kimai Compose container uses:

```yaml
security_opt:
  - no-new-privileges:true
```

The container also has:

* Health check
* Restart policy
* Private Docker network connectivity
* Persistent application volumes

Services that require host access are bound to localhost.

The database is not exposed on an external network interface.

Credentials are supplied through environment variables rather than hard-coded directly into the Compose configuration.

---

# 12. Docker Image Versioning and Rollback

The deployed Kimai image is:

```text
sxnthosh/kimai-devops:1.0.0
```

A test version tag was also created:

```text
sxnthosh/kimai-devops:1.0.1
```

The version transition was tested by recreating the Kimai container without removing persistent volumes.

The rollback procedure was also tested successfully by returning the deployment from `1.0.1` to `1.0.0`.

Example deployment command:

```bash
docker compose up -d --no-deps --force-recreate kimai
```

After a version change, deployment verification includes:

```bash
docker compose ps
```

Container health:

```bash
docker inspect kimai_app \
  --format='{{.State.Health.Status}}'
```

Application availability:

```bash
curl -I http://127.0.0.1:8000
```

The verified rollback returned the Kimai container to:

```text
sxnthosh/kimai-devops:1.0.0
```

with the container healthy and the application returning HTTP `302 Found`.

---

# 13. CI/CD

GitHub Actions is the implemented CI/CD system.

The workflow is triggered by:

```text
Push to main
Pull request to main
```

The validation stage performs Docker Compose validation.

The deployment stage runs on the configured self-hosted runner and performs:

```text
Checkout / update repository
        |
        v
Pull Docker images
        |
        v
Start Docker Compose stack
        |
        v
Verify Kimai
        |
        v
Verify MariaDB
        |
        v
Verify Prometheus
        |
        v
Verify Grafana
        |
        v
Deployment summary
```

The GitHub Actions deployment workflow has been successfully executed.

The project also contains a `Jenkinsfile` because Jenkins was included in the original project requirements. Jenkins itself is not running as part of the current local infrastructure.

---

# 14. Backup and Recovery

MariaDB uses persistent Docker storage.

The project maintains database backup and restoration procedures.

Backup and restore documentation is provided in:

```text
BACKUP_RESTORE.md
```

Backup scripts are maintained under:

```text
scripts/
```

Database restoration has been tested successfully.

Application and monitoring persistent volumes include:

```text
mariadb_data
kimai_var
kimai_public
grafana_data
```

Normal application deployment and rollback operations do not require removing these volumes.

The following command should not be used for normal restarts or deployments:

```bash
docker compose down -v
```

because it removes persistent Docker volumes.

---

# 15. Cloud Requirement Mapping

The original project specification includes cloud-oriented requirements such as:

* AWS/GCP multi-cloud architecture
* AWS S3 Terraform remote backend
* Application Load Balancer
* WAF
* Bastion host
* IAM roles and policies
* Cloud security groups
* Cloud cost estimation

These resources are not deployed in the current local/on-premise environment.

The following local equivalents are implemented where practical:

| Cloud Requirement       | Local Implementation                              |
| ----------------------- | ------------------------------------------------- |
| Cloud compute           | Docker containers                                 |
| Cloud networking        | Docker bridge network                             |
| Security Groups         | Localhost port binding + Docker network isolation |
| Managed monitoring      | Prometheus + Grafana                              |
| Container monitoring    | cAdvisor                                          |
| Host monitoring         | Node Exporter                                     |
| Cloud CI/CD             | GitHub Actions                                    |
| Cloud image registry    | Docker Hub                                        |
| Cloud database          | MariaDB container                                 |
| Persistent storage      | Docker volumes                                    |
| Cloud backup            | Local MariaDB backup                              |
| Cloud Terraform backend | Local Terraform state                             |

The following cloud controls remain future deployment requirements:

| Cloud Feature                 | Current Status |
| ----------------------------- | -------------- |
| AWS IAM                       | Not deployed   |
| AWS WAF                       | Not deployed   |
| AWS Application Load Balancer | Not deployed   |
| AWS Bastion Host              | Not deployed   |
| AWS Security Groups           | Not deployed   |
| AWS S3 Terraform backend      | Not deployed   |
| AWS Auto Scaling              | Not deployed   |
| AWS CloudWatch                | Not deployed   |

These limitations are intentional because the current project environment is local/on-premise and does not provision AWS infrastructure.

---

# 16. Network and Port Summary

## Docker Compose Stack

| Service       | Host Binding     | Container Port |
| ------------- | ---------------- | -------------: |
| Kimai         | `127.0.0.1:8000` |           8001 |
| MariaDB       | `127.0.0.1:3307` |           3306 |
| Prometheus    | `127.0.0.1:9090` |           9090 |
| Grafana       | `127.0.0.1:3000` |           3000 |
| cAdvisor      | `127.0.0.1:8080` |           8080 |
| Node Exporter | Internal         |           9100 |

## Terraform Stack

| Service    | Host Binding     | Container Port |
| ---------- | ---------------- | -------------: |
| Kimai      | `127.0.0.1:8002` |           8001 |
| MariaDB    | `127.0.0.1:3308` |           3306 |
| Prometheus | `127.0.0.1:9091` |           9090 |
| Grafana    | `127.0.0.1:3001` |           3000 |

---

# 17. Implementation Verification

The following components have been verified during implementation:

```text
Kimai container                    ✅
MariaDB container                  ✅
Docker Compose                     ✅
Persistent Docker volumes          ✅
Kimai health check                 ✅
Prometheus                         ✅
Node Exporter                      ✅
cAdvisor                           ✅
Grafana                            ✅
Kimai Monitoring dashboard         ✅
High CPU alert                     ✅
Low Disk Space alert               ✅
Kimai Application Health alert     ✅
Grafana email notification test    ✅
Terraform Docker infrastructure    ✅
Docker image 1.0.0                 ✅
Docker image 1.0.1 test tag        ✅
Image rollback                     ✅
Docker Hub image push              ✅
GitHub Actions deployment          ✅
Database backup                    ✅
Database restore test              ✅
```

---

# 18. Final Architecture Summary

The implemented platform follows this local deployment architecture:

```text
                    GitHub
                       |
                       v
                GitHub Actions
                       |
                       v
                   Docker Hub
                       |
                       v
              Docker Compose
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
      Kimai          MariaDB       Monitoring
        |                             |
        |                       +-----+-----+
        |                       |           |
        |                       v           v
        |                  Prometheus    Grafana
        |                       ^
        |                       |
        +-----------------------+
                                |
                       Node Exporter
                       cAdvisor
```

The application, database, infrastructure provisioning, CI/CD, monitoring, alerting, security controls, backup procedures, and rollback workflow are all represented in the project implementation.

The architecture is designed so that the local implementation can later be mapped to cloud infrastructure without changing the fundamental application and monitoring design.
