output "kimai_url" {
  description = "Kimai application URL"
  value       = "http://127.0.0.1:8002"
}

output "kimai_health_url" {
  description = "Kimai application health URL"
  value       = "http://127.0.0.1:8002"
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
