output "container_name" {
  description = "Kimai container name"
  value       = docker_container.kimai.name
}

output "url" {
  description = "Kimai application URL"
  value       = "http://127.0.0.1:8002"
}

output "health_url" {
  description = "Kimai application health URL"
  value       = "http://127.0.0.1:8002"
}
