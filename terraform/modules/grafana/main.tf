resource "docker_image" "grafana" {
  name = "grafana/grafana:10.4.0"
}

resource "docker_volume" "grafana_data" {
  name = "python-devops-terraform-grafana-data"
}

resource "docker_container" "grafana" {
  name  = "terraform-grafana"
  image = docker_image.grafana.image_id

  restart = "unless-stopped"

  ports {
    internal = 3000
    external = 3001
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name = var.network_name
  }

  volumes {
    volume_name    = docker_volume.grafana_data.name
    container_path = "/var/lib/grafana"
  }
}
