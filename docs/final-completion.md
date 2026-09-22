# Final Project Completion and Cloud Requirement Mapping

## Project status

This project implements a production-style local DevOps environment for Kimai using Docker, Docker Compose, MariaDB, Nginx, Terraform, Prometheus, Grafana, GitHub Actions and Jenkins.

The implementation is intentionally local/on-premises. AWS/GCP resources are not claimed as deployed resources.

## Implemented components

- Kimai application container
- MariaDB database
- Persistent Docker volumes
- Docker network isolation
- Nginx reverse proxy/load-balancer
- Two Kimai application instances for local HA demonstration
- Prometheus monitoring
- Grafana dashboards
- Node Exporter infrastructure metrics
- cAdvisor container metrics
- CPU, disk and application health alerts
- Docker health checks
- Terraform infrastructure provisioning
- Docker image versioning
- Image rollback testing
- GitHub Actions CI/CD
- Jenkins CI/CD
- Secure Jenkins secret-file injection
- Backup archives before HA changes
- Git repository and documentation

## Cloud requirement mapping

| Cloud requirement | Local implementation |
|---|---|
| AWS/GCP compute | Docker containers |
| Application Load Balancer | Nginx reverse proxy |
| Auto Scaling Group | Multiple Kimai containers |
| Security Groups | Docker network and published-port restrictions |
| AWS WAF | Not deployed; WAF is a documented next cloud-layer component |
| Bastion Host | Local administrative access controls |
| IAM | Least-privilege application/database credentials |
| S3 remote Terraform backend | Not deployed; Terraform uses local state |
| CloudWatch | Prometheus + Grafana |
| ELK centralized logging | Docker/container logs; centralized logging is a documented extension |
| Cloud backup | Docker-volume/database backup archives |

## High availability

Two Kimai containers are placed behind Nginx:

- `kimai_app`
- `kimai_app_2`

Both connect to the MariaDB service.

Nginx provides the reverse-proxy/load-balancing layer.

The application instances use separate writable application volumes to avoid simultaneous direct writes to the same Docker volume.

For production cloud deployment, shared session storage, shared file storage and database high availability should additionally be configured.

## Security

Implemented:

- Secrets kept outside Git
- `.env` ignored by Git
- Terraform variable files ignored
- Database credentials are supplied through environment/secret mechanisms
- `no-new-privileges:true` enabled for application containers
- MariaDB is not exposed directly to the public network
- Kimai is bound to localhost
- Nginx is used as the application entry point
- Health checks validate application and database availability

## Monitoring

Prometheus collects infrastructure and container metrics.

Grafana provides:

- CPU usage
- Memory usage
- Disk usage
- Network receive traffic
- Network transmit traffic

Alerts:

1. High CPU usage
2. Low disk space
3. Kimai application health failure

## Backup and recovery

Backups were created before the HA changes:

- `backups/kimai_public_before_ha.tar.gz`
- `backups/kimai_var_before_ha.tar.gz`

The database backup/restore procedure was previously tested.

Production deployment should additionally use scheduled database backups, off-host storage and periodic restore testing.

## CI/CD

GitHub Actions validates Docker Compose and performs deployment validation.

Jenkins provides an additional CI/CD pipeline with:

- SCM checkout
- secret injection
- Docker Compose validation
- image pulling
- deployment
- application health validation
- database health validation
- Prometheus validation
- Grafana validation

## Final limitation

The original assignment contains AWS-specific requirements. Because this implementation is intentionally local and no AWS account/resources are being used, AWS WAF, ALB, IAM, ASG and S3 are represented by documented local equivalents rather than falsely reported as deployed AWS resources.

A future cloud deployment can map these components directly to AWS managed services.
