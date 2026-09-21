resource "docker_image" "mariadb" {
  name = "mariadb:11.2.2"
}

resource "docker_volume" "mariadb_data" {
  name = "python-devops-terraform-mariadb-data"
}

resource "docker_container" "mariadb" {
  name  = "terraform-devops-mariadb"
  image = docker_image.mariadb.image_id

  restart = "unless-stopped"

  env = [
    "MARIADB_ROOT_PASSWORD=${var.db_root_password}",
    "MARIADB_DATABASE=${var.db_name}",
    "MARIADB_USER=${var.db_user}",
    "MARIADB_PASSWORD=${var.db_password}"
  ]

  ports {
    internal = 3306
    external = 3308
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = var.network_name
  }

  volumes {
    volume_name    = docker_volume.mariadb_data.name
    container_path = "/var/lib/mysql"
  }
}
