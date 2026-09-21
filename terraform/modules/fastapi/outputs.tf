output "container_name" {
  description = "FastAPI container name"
  value       = docker_container.fastapi.name
}

output "url" {
  description = "FastAPI application URL"
  value       = "http://127.0.0.1:8001"
}

output "health_url" {
  description = "FastAPI health endpoint"
  value       = "http://127.0.0.1:8001/health"
}
