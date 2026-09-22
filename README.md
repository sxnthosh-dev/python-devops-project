# Kimai DevOps Time Tracking Platform

A containerized DevOps project for deploying and operating the open-source **Kimai time-tracking application** with MariaDB, Docker Compose, Terraform, Prometheus, Grafana, Docker Hub, and GitHub Actions.

The project demonstrates infrastructure provisioning, containerization, security configuration, monitoring, alerting, CI/CD, database backup and restore, Docker image versioning, and application rollback.

The implementation runs locally/on-premise using Docker rather than AWS or GCP cloud infrastructure. Cloud-specific requirements that cannot be implemented locally are documented as limitations and future deployment mappings.

---

## Architecture

```text
                         Developer
                            |
                            v
                     Git / GitHub
                            |
                            v
                  GitHub Actions CI/CD
                            |
                            v
                       Docker Hub
                  Versioned Kimai Image
                            |
                 +----------+----------+
                 |                     |
                 v                     v
          Docker Compose          Terraform
          Local Deployment      Docker Infrastructure
                 |                     |
                 +----------+----------+
                            |
                    Docker Bridge Network
                       internal-network
                            |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
     Kimai               MariaDB           Monitoring
   kimai_app          devops-mariadb          Stack
        |                   |              +----+----+
        |                   |              |         |
        |                   |              v         v
        |                   |         Prometheus   Grafana
        |                   |              |         |
        +-------------------+--------------+------> Alerts
```

---

## Technology Stack

| Area                     | Technology                               |
| ------------------------ | ---------------------------------------- |
| Application              | Kimai                                    |
| Database                 | MariaDB 11.2.2                           |
| Containerization         | Docker                                   |
| Orchestration            | Docker Compose                           |
| Infrastructure as Code   | Terraform                                |
| Metrics                  | Prometheus                               |
| Host metrics             | Node Exporter                            |
| Container metrics        | cAdvisor                                 |
| Visualization & Alerting | Grafana 10.4.0                           |
| Source Control           | Git / GitHub                             |
| CI/CD                    | GitHub Actions                           |
| Container Registry       | Docker Hub                               |
| Backup                   | MariaDB dump + persistent Docker volumes |

---

## Project Features

### Application

* Kimai time-tracking application
* MariaDB persistent database
* Dockerized application deployment
* HTTP health verification
* Persistent application volumes
* Restart policies

### Container Security

* Docker `no-new-privileges:true` for the Kimai container
* Database bound to localhost
* Application bound to localhost
* Prometheus and Grafana bound to localhost
* Credentials supplied through environment configuration
* `.env` and Terraform variable files excluded from Git
* Private Docker bridge network for service-to-service communication

> The official Kimai image's default user configuration is retained. The project Dockerfile is a thin wrapper around the official Kimai image and should not be described as a custom multi-stage/non-root Dockerfile.

### Monitoring

Prometheus collects infrastructure metrics from:

* Node Exporter
* cAdvisor

Grafana provides the **Kimai Monitoring** dashboard with:

1. CPU Usage
2. Memory Usage
3. Disk Usage
4. Network Receive
5. Network Transmit

### Alerting

Three Grafana alert rules are configured:

* **Kimai High CPU Usage**
* **Kimai Low Disk Space**
* **Kimai Application Health Failure**

The alert rules use a 5-minute pending period and are evaluated every 10 seconds.

A Grafana email contact point has also been configured and tested successfully.

---

## Docker Image Versioning

The Kimai application uses a versioned Docker image:

```text
sxnthosh/kimai-devops:1.0.0
```

A second test/release tag was created:

```text
sxnthosh/kimai-devops:1.0.1
```

The image versioning workflow was tested successfully.

### Upgrade test

```text
1.0.0
  |
  v
1.0.1
  |
  +-- Container healthy
  +-- HTTP 302 response
  +-- Persistent volumes preserved
```

### Rollback test

```text
1.0.1
  |
  v
1.0.0
  |
  +-- Container healthy
  +-- HTTP 302 response
  +-- Persistent volumes preserved
```

The verified `1.0.0` image was pushed to Docker Hub and successfully pulled by the GitHub Actions deployment runner.

---

## CI/CD

GitHub Actions is the CI/CD implementation used for the actual deployment.

The workflow performs:

1. Checkout
2. Docker Compose validation
3. Deployment on the self-hosted runner
4. Docker image pull
5. Docker Compose startup
6. Kimai readiness verification
7. Kimai container health verification
8. MariaDB health verification
9. Prometheus verification
10. Grafana verification
11. Deployment summary

The GitHub Actions workflow has been executed successfully with a **green/passed result**.

### CI/CD flow

```text
Git push to main
       |
       v
GitHub Actions
       |
       v
Validate Docker Compose
       |
       v
Self-hosted runner
       |
       v
Pull versioned Docker images
       |
       v
docker compose up -d
       |
       +---- Kimai health
       +---- MariaDB health
       +---- Prometheus health
       +---- Grafana availability
       |
       v
Deployment successful
```

A `Jenkinsfile` is also maintained for the project because Jenkins was part of the original project requirements. Jenkins itself was not executed in the local implementation.

---

## Environment Configuration

Create the local environment file from the example:

```bash
cp .env.example .env
```

The actual `.env` file must contain the required database, Kimai, and application secrets.

Never commit `.env` to Git.

The repository `.gitignore` excludes:

```text
.env
terraform/*.tfvars
```

Secrets should never be pasted into source control, documentation, or public repositories.

---

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd python-devops-project
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with appropriate local credentials.

### 3. Start the Docker Compose stack

```bash
docker compose up -d
```

### 4. Check the services

```bash
docker compose ps
```

Expected services include:

```text
kimai_app
devops-mariadb
prometheus
grafana
node-exporter
cadvisor
```

### 5. Verify Kimai

```bash
curl -I http://127.0.0.1:8000
```

A successful deployment returns an HTTP redirect to the Kimai homepage:

```text
HTTP/1.1 302 Found
Location: /en/homepage
```

### 6. Stop the stack

```bash
docker compose stop
```

### 7. Start the existing stack again

```bash
docker compose start
```

> Avoid `docker compose down -v` unless you intentionally want to remove persistent Docker volumes.

---

## Service URLs

| Service       | URL                                    |
| ------------- | -------------------------------------- |
| Kimai         | `http://127.0.0.1:8000`                |
| Prometheus    | `http://127.0.0.1:9090`                |
| Grafana       | `http://127.0.0.1:3000`                |
| cAdvisor      | `http://127.0.0.1:8080`                |
| Node Exporter | Internal Docker network on port `9100` |

The Terraform-created infrastructure uses separate host ports:

| Service    | Terraform URL           |
| ---------- | ----------------------- |
| Kimai      | `http://127.0.0.1:8002` |
| Prometheus | `http://127.0.0.1:9091` |
| Grafana    | `http://127.0.0.1:3001` |

---

## Terraform

Terraform provisions Docker-based local infrastructure.

Resources include:

* Docker network
* MariaDB
* Kimai
* Prometheus
* Grafana

Initialize Terraform:

```bash
cd terraform
terraform init
```

Validate:

```bash
terraform validate
```

Review the plan:

```bash
terraform plan -var-file="terraform.tfvars"
```

Apply infrastructure:

```bash
terraform apply -var-file="terraform.tfvars"
```

View outputs:

```bash
terraform output
```

Current Terraform outputs include:

```text
kimai_url
kimai_health_url
prometheus_url
grafana_url
mariadb_host
docker_network
```

### Terraform backend limitation

The original cloud-oriented requirement called for an S3 remote backend.

This implementation does not use an AWS S3 backend because the project is deployed locally/on-premise. Terraform uses local state for this environment.

---

## Monitoring

### Prometheus

Prometheus scrapes:

```text
node-exporter:9100
cadvisor:8080
```

Prometheus configuration is located at:

```text
prometheus/prometheus.yml
```

### Grafana

Grafana uses Prometheus as its data source.

Dashboard:

```text
Kimai Monitoring
```

Dashboard panels:

* CPU Usage
* Memory Usage
* Disk Usage
* Network Receive
* Network Transmit

---

## Grafana Alerts

### High CPU

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

Threshold:

```text
Above 80%
```

Pending period:

```text
5 minutes
```

### Low Disk Space

The rule monitors available filesystem capacity and triggers when available space falls below the configured threshold.

Threshold:

```text
Below 20%
```

Pending period:

```text
5 minutes
```

### Kimai Application Health

The application health rule uses container monitoring information to detect when the Kimai application is no longer being reported as expected.

Pending period:

```text
5 minutes
```

---

## Backup and Restore

MariaDB data is stored in a persistent Docker volume.

The project contains backup and restoration documentation:

```text
BACKUP_RESTORE.md
```

Backup scripts are available under:

```text
scripts/
```

The existing database backup/restore workflow has been tested.

Do not remove the MariaDB volume when performing normal application restarts or deployments.

---

## Security

Security measures implemented in the local environment include:

* Secrets stored in `.env`
* `.env` excluded from Git
* Terraform variable files excluded from Git
* MariaDB bound to `127.0.0.1`
* Kimai bound to `127.0.0.1`
* Prometheus bound to `127.0.0.1`
* Grafana bound to `127.0.0.1`
* Private Docker bridge network
* `no-new-privileges:true` on Kimai
* Container health checks
* Restart policies
* Versioned Docker images
* Database backup capability

### Cloud security limitations

The following cloud-specific controls are not deployed in the local environment:

* AWS IAM roles/policies
* AWS WAF
* AWS Security Groups
* Public Application Load Balancer
* Bastion host
* AWS Auto Scaling Groups
* AWS S3 remote Terraform backend

These requirements are documented in the architecture documents as future cloud deployment mappings.

---

## Docker Rollback Procedure

The project uses explicit Docker image versions rather than relying on an untracked application state.

To switch to a previously verified image version, update the Kimai image in:

```text
docker-compose.yml
```

For example:

```yaml
kimai:
  image: sxnthosh/kimai-devops:1.0.0
```

Then recreate only the Kimai service:

```bash
docker compose up -d --no-deps --force-recreate kimai
```

Verify:

```bash
docker inspect kimai_app \
  --format='Image: {{.Config.Image}}'
```

Check health:

```bash
docker inspect kimai_app \
  --format='Health: {{.State.Health.Status}}'
```

Check HTTP availability:

```bash
curl -I http://127.0.0.1:8000
```

The rollback from `1.0.1` to `1.0.0` was successfully tested in this project.

---

## Backup and Rollback Safety

Normal deployments should not remove persistent volumes.

Avoid:

```bash
docker compose down -v
```

unless permanent removal of application/database data is intentionally required.

The normal deployment/rollback operation recreates the application container while retaining:

```text
kimai_var
kimai_public
mariadb_data
grafana_data
```

---

## Project Documentation

| Document                    | Purpose                                     |
| --------------------------- | ------------------------------------------- |
| `README.md`                 | Project overview and operating instructions |
| `docs/high-level-design.md` | High-level architecture                     |
| `docs/low-level-design.md`  | Detailed technical design                   |
| `BACKUP_RESTORE.md`         | Database backup and restore                 |
| `Dockerfile`                | Kimai container image definition            |
| `docker-compose.yml`        | Local service orchestration                 |
| `Jenkinsfile`               | Jenkins pipeline definition                 |
| `.github/workflows/ci.yml`  | GitHub Actions CI/CD                        |
| `prometheus/prometheus.yml` | Prometheus configuration                    |
| `terraform/`                | Infrastructure as Code                      |

---

## Project Structure

```text
python-devops-project/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── high-level-design.md
│   └── low-level-design.md
│
├── grafana/
│   └── grafana.ini
│
├── monitoring/
│   └── prometheus.yml
│
├── prometheus/
│   └── prometheus.yml
│
├── terraform/
│   ├── main.tf
│   ├── network.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── moved.tf
│
├── scripts/
│   ├── backup.sh
│   ├── deploy.sh
│   ├── healthcheck.sh
│   └── setup.sh
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── BACKUP_RESTORE.md
├── .env.example
├── .gitignore
└── README.md
```

The repository also contains files from the project's earlier FastAPI development stage. Those files are retained as project history and are not the final deployed application.

---

## Verification Summary

The final implementation has been verified for:

```text
Git repository clean                 ✅
Docker Compose stack healthy         ✅
Kimai container healthy              ✅
MariaDB container healthy            ✅
Prometheus healthy                   ✅
Grafana reachable                    ✅
Terraform outputs available          ✅
Docker image 1.0.0 versioned         ✅
Docker image 1.0.1 upgrade tested    ✅
Rollback to 1.0.0 tested             ✅
Docker volumes preserved             ✅
Docker image pushed to Docker Hub    ✅
GitHub Actions CI/CD passed          ✅
Grafana alerts configured            ✅
Database backup/restore tested       ✅
```

---

## Cloud Deployment Considerations

The original assignment includes AWS/GCP-oriented infrastructure requirements.

This project intentionally uses a local/on-premise Docker implementation instead of provisioning paid cloud resources.

The architecture documents identify how the local components could map to cloud services in a future deployment, including:

* Docker services → cloud compute/container services
* Docker bridge network → cloud private networking
* Local persistent volumes → cloud managed storage
* Prometheus/Grafana → managed or self-hosted observability
* Local secrets → cloud secret management
* Local Terraform state → remote backend
* Local security controls → cloud IAM/security groups/WAF/load balancer

No AWS resources are claimed as deployed by this project.

---

## License

This project is intended for educational, portfolio, and DevOps infrastructure demonstration purposes.
