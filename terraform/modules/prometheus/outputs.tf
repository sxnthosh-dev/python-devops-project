output "container_name" {
  description = "Prometheus container name"
  value       = docker_container.prometheus.name
}

output "url" {
  description = "Prometheus URL"
  value       = "http://127.0.0.1:9091"
}
