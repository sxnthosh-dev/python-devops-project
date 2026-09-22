# Low-Level Design (LLD)

# Kimai DevOps Time Tracking Platform

## 1. Document Overview

This document provides the detailed technical design of the implemented
Kimai DevOps platform.

The system is deployed locally using Docker, Docker Compose, and
Terraform.

---

# 2. Service Architecture

| Service       | Image                              | Container        | Host Port | Container Port |
| ------------- | ---------------------------------- | ---------------- | --------: | -------------: |
| Kimai         | `kimai/kimai2:stable`              | `kimai_app`      |      8000 |           8001 |
| MariaDB       | `mariadb:11.2.2`                   | `devops-mariadb` |      3307 |           3306 |
| Prometheus    | `prom/prometheus:v2.51.0`          | `prometheus`     |      9090 |           9090 |
| Grafana       | `grafana/grafana:10.4.0`           | `grafana`        |      3000 |           3000 |
| Node Exporter | `prom/node-exporter:v1.8.1`        | `node-exporter`  |  Internal |           9100 |
| cAdvisor      | `gcr.io/cadvisor/cadvisor:v0.49.1` | `cadvisor`       |      8080 |           8080 |

The Compose services communicate through the `internal-network` Docker
bridge network.

---

# 3. Kimai Application

## 3.1 Container

| Property        | Value                    |
| --------------- | ------------------------ |
| Image           | `kimai/kimai2:stable`    |
| Container       | `kimai_app`              |
| Internal port   | 8001                     |
| Host binding    | `127.0.0.1:8000`         |
| Restart policy  | `unless-stopped`         |
| Health check    | Enabled                  |
| Security option | `no-new-privileges:true` |

The health check verifies the Kimai HTTP service:

```text
curl -f http://127.0.0.1:8001
```

The container has been verified as healthy and responds with HTTP 302 to
the Kimai homepage.

The official Kimai image's default user configuration is retained rather
than forcing a user override that could interfere with the image's
entrypoint and filesystem permissions.

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

Kimai connects to MariaDB using the Docker service name:

```text
db:3306
```

The database is not exposed on the external network interface.

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

Application and monitoring services communicate through this private
Docker network.

Host port bindings use `127.0.0.1` for services that need host access.

---

# 6. Monitoring

## 6.1 Prometheus

Prometheus runs on:

```text
127.0.0.1:9090
```

The Compose Prometheus configuration scrapes:

```yaml
- job_name: "node"
  static_configs:
    - targets: ["node-exporter:9100"]

- job_name: "cadvisor"
  static_configs:
    - targets: ["cadvisor:8080"]
```

The targets have been verified as healthy.

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

---

## 6.3 cAdvisor

cAdvisor exposes container metrics on:

```text
cadvisor:8080
```

It is used to provide container monitoring data to Prometheus.

---

# 7. Grafana

Grafana runs on:

```text
127.0.0.1:3000
```

Prometheus is configured as the Grafana data source.

The main dashboard is:

```text
Kimai Monitoring
```

Dashboard panels:

### Panel 1 — CPU Usage

```promql
100 - (
  avg by(instance) (
    rate(node_cpu_seconds_total{job="node",mode="idle"}[5m])
  ) * 100
)
```

### Panel 2 — Memory Usage

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

### Panel 3 — Disk Usage

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

### Panel 4 — Network Receive

```promql
sum by(device) (
  rate(node_network_receive_bytes_total{job="node"}[5m])
)
```

### Panel 5 — Network Transmit

```promql
sum by(device) (
  rate(node_network_transmit_bytes_total{job="node"}[5m])
)
```

---

# 8. Grafana Alert Rules

## 8.1 High CPU

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

---

## 8.2 Low Disk Space

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

---

## 8.3 Kimai Application Health

The application health rule monitors the presence of the Kimai
application container through cAdvisor.

The alert fires when the expected Kimai container monitoring metric is no
longer available.

Pending period:

```text
5 minutes
```

---

# 9. Terraform Infrastructure

Terraform uses the Docker provider to provision the local infrastructure.

Major Terraform modules:

```text
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── moved.tf
└── modules/
    ├── network/
    ├── database/
    ├── fastapi/
    ├── prometheus/
    └── grafana/
```

The existing `fastapi` module directory is retained for Terraform module
compatibility, but the deployed application resource has been migrated
to Kimai.

The Terraform application resource is:

```text
terraform-kimai-app
```

Terraform-managed service ports include:

| Service    | Host Port |
| ---------- | --------: |
| Kimai      |      8002 |
| MariaDB    |      3308 |
| Prometheus |      9091 |
| Grafana    |      3001 |

These are separate from the Docker Compose monitoring stack.

---

# 10. Terraform Security

Terraform variables containing credentials are marked sensitive where
appropriate.

Credential files such as:

```text
terraform/*.tfvars
```

are excluded from Git.

The `.env` file is also excluded from Git.

Only the example environment configuration is tracked.

---

# 11. Container Security

The Kimai Compose container uses:

```yaml
security_opt:
  - no-new-privileges:true
```

The container also has a health check and restart policy.

Services that require host access are bound to localhost.

The database is not exposed to external network interfaces.

---

# 12. CI/CD

GitHub Actions is used for the implemented CI/CD workflow.

The workflow validates the project on pushes and pull requests to the
main branch.

The project also contains a Jenkinsfile to satisfy the requested Jenkins
pipeline design.

Jenkins execution is not part of the local running infrastructure.

---

# 13. Backup and Rollback

MariaDB uses persistent Docker storage.

Database backups are maintained separately and restore testing has been
performed.

Docker image versioning provides rollback capability.

A previously tested image tag can be deployed if the current application
version needs to be reverted.

---

# 14. Cloud Requirement Mapping

The project specification includes cloud-specific requirements such as:

* AWS/GCP multi-cloud architecture
* AWS S3 Terraform remote backend
* Application Load Balancer
* WAF
* Bastion host
* IAM roles
* Cloud cost estimation

These are not deployed in the current local environment.

The local implementation provides equivalent architectural concepts
where possible:

| Cloud Requirement      | Local Equivalent                                |
| ---------------------- | ----------------------------------------------- |
| Cloud compute          | Docker containers                               |
| Cloud networking       | Docker bridge network                           |
| Security Groups        | Local port binding and Docker network isolation |
| Managed monitoring     | Prometheus + Grafana                            |
| Container monitoring   | cAdvisor                                        |
| Object/database backup | Local database backup                           |
| Cloud CI/CD            | GitHub Actions                                  |
| Cloud image registry   | Docker Hub                                      |

Cloud-specific resources should be provisioned separately if the project
is later migrated to AWS or another cloud platform.
