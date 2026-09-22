
module "network" {
  source = "./modules/network"

  network_name = var.network_name
}

module "database" {
  source = "./modules/database"

  db_root_password = var.db_root_password
  db_name          = var.kimai_db_name
  db_user          = var.kimai_db_user
  db_password      = var.kimai_db_password
  network_name     = module.network.network_name
}

module "fastapi" {
  source = "./modules/fastapi"

  image          = "kimai/kimai2:stable"
  db_host        = module.database.container_name
  db_port        = "3306"
  db_name        = var.kimai_db_name
  db_user        = var.kimai_db_user
  db_password    = var.kimai_db_password
  network_name   = module.network.network_name
  app_secret     = var.kimai_app_secret
  trusted_hosts  = var.kimai_trusted_hosts
  admin_email    = var.kimai_admin_email
  admin_password = var.kimai_admin_password
}
module "prometheus" {
  source = "./modules/prometheus"

  network_name = module.network.network_name
}

module "grafana" {
  source = "./modules/grafana"

  network_name = module.network.network_name
}