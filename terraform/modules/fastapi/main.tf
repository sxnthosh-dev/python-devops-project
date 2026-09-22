resource "docker_image" "kimai" {
  name = var.image
}

resource "docker_container" "kimai" {
  name    = "terraform-kimai-app"
  image   = docker_image.kimai.image_id
  restart = "unless-stopped"

  env = [
    "DATABASE_URL=mysql://${var.db_user}:${var.db_password}@${var.db_host}:${var.db_port}/${var.db_name}?charset=utf8mb4&serverVersion=11.2.2-MariaDB",
    "APP_SECRET=${var.app_secret}",
    "TRUSTED_HOSTS=${var.trusted_hosts}",
    "ADMINMAIL=${var.admin_email}",
    "ADMINPASS=${var.admin_password}"
  ]

  ports {
    internal = 8001
    external = 8002
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = var.network_name
  }

  security_opts = [
    "no-new-privileges:true"
  ]

  healthcheck {
    test     = ["CMD", "curl", "-f", "http://127.0.0.1:8001"]
    interval = "30s"
    timeout  = "10s"
    retries  = 3
  }

  memory      = 1024
  memory_swap = 2048
  cpus        = "1.0"
}
