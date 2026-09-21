resource "docker_image" "fastapi" {
  name = var.image
}

resource "docker_container" "fastapi" {
  name  = "terraform-fastapi-app"
  image = docker_image.fastapi.image_id

  restart = "unless-stopped"

  env = [
    "DB_HOST=${var.db_host}",
    "DB_PORT=${var.db_port}",
    "DB_NAME=${var.db_name}",
    "DB_USER=${var.db_user}",
    "DB_PASSWORD=${var.db_password}"
  ]

  ports {
    internal = 8000
    external = 8001
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = var.network_name
  }

  security_opts = [
    "no-new-privileges:true"
  ]

  healthcheck {
    test = [
      "CMD",
      "python",
      "-c",
      "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
    ]
    interval = "30s"
    timeout  = "10s"
    retries  = 3
  }

  memory      = 512
  memory_swap = 1024
  cpus        = "1.0"
  user        = "appuser"
  working_dir = "/app"
}