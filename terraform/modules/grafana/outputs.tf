output "container_name" {
  description = "Grafana container name"
  value       = docker_container.grafana.name
}

output "url" {
  description = "Grafana URL"
  value       = "http://127.0.0.1:3001"
}

output "volume_name" {
  description = "Grafana persistent volume name"
  value       = docker_volume.grafana_data.name
}
