resource "docker_image" "prometheus" {
  name = "prom/prometheus:v2.51.0"
}

resource "docker_container" "prometheus" {
  name  = "terraform-prometheus"
  image = docker_image.prometheus.image_id

  restart = "unless-stopped"

  ports {
    internal = 9090
    external = 9091
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = var.network_name
  }

  volumes {
    host_path      = abspath("${path.root}/prometheus.yml")
    container_path = "/etc/prometheus/prometheus.yml"
    read_only      = true
  }

  command = [
    "--config.file=/etc/prometheus/prometheus.yml"
  ]
}
