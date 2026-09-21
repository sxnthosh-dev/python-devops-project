
module "network" {
  source = "./modules/network"

  network_name = var.network_name
}

module "database" {
  source = "./modules/database"

  db_root_password = var.db_root_password
  db_name          = var.db_name
  db_user          = var.db_user
  db_password      = var.db_password
  network_name     = module.network.network_name
}

module "fastapi" {
  source = "./modules/fastapi"

  image        = "sxnthosh/python-devops-project:latest"
  db_host      = module.database.container_name
  db_port      = "3306"
  db_name      = var.db_name
  db_user      = var.db_user
  db_password  = var.db_password
  network_name = module.network.network_name
}
module "prometheus" {
  source = "./modules/prometheus"

  network_name = module.network.network_name
}

module "grafana" {
  source = "./modules/grafana"

  network_name = module.network.network_name
}