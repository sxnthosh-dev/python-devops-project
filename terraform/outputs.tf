output "fastapi_url" {
  description = "FastAPI application URL"
  value       = "http://127.0.0.1:8001"
}

output "fastapi_health_url" {
  description = "FastAPI health endpoint"
  value       = "http://127.0.0.1:8001/health"
}

output "prometheus_url" {
  description = "Prometheus URL"
  value       = "http://127.0.0.1:9091"
}

output "grafana_url" {
  description = "Grafana URL"
  value       = "http://127.0.0.1:3001"
}

output "mariadb_host" {
  description = "MariaDB container hostname on the Terraform Docker network"
  value       = module.database.container_name
}

output "docker_network" {
  description = "Terraform-managed Docker network"
  value       = module.network.network_name
}