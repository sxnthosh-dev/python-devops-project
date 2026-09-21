moved {
  from = docker_network.app_network
  to   = module.network.docker_network.app_network
}

moved {
  from = docker_image.mariadb
  to   = module.database.docker_image.mariadb
}

moved {
  from = docker_volume.mariadb_data
  to   = module.database.docker_volume.mariadb_data
}

moved {
  from = docker_container.mariadb
  to   = module.database.docker_container.mariadb
}

moved {
  from = docker_image.fastapi
  to   = module.fastapi.docker_image.fastapi
}

moved {
  from = docker_container.fastapi
  to   = module.fastapi.docker_container.fastapi
}

moved {
  from = docker_image.prometheus
  to   = module.prometheus.docker_image.prometheus
}

moved {
  from = docker_container.prometheus
  to   = module.prometheus.docker_container.prometheus
}

moved {
  from = docker_image.grafana
  to   = module.grafana.docker_image.grafana
}

moved {
  from = docker_volume.grafana_data
  to   = module.grafana.docker_volume.grafana_data
}

moved {
  from = docker_container.grafana
  to   = module.grafana.docker_container.grafana
}