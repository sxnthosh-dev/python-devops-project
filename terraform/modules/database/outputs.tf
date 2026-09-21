output "container_name" {
  description = "MariaDB container name"
  value       = docker_container.mariadb.name
}

output "volume_name" {
  description = "MariaDB persistent volume name"
  value       = docker_volume.mariadb_data.name
}
