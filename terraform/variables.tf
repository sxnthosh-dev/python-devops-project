variable "project_name" {
  description = "Project name used for Terraform-managed Docker resources"
  type        = string
  default     = "python-devops-project"
}

variable "network_name" {
  description = "Docker network name"
  type        = string
  default     = "python-devops-terraform-network"
}

variable "db_root_password" {
  description = "MariaDB root password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Legacy database name"
  type        = string
  default     = "devops_db"
}

variable "db_user" {
  description = "Legacy database user"
  type        = string
  default     = "devuser"
}

variable "db_password" {
  description = "Legacy database password"
  type        = string
  sensitive   = true
}

variable "kimai_db_name" {
  description = "Kimai database name"
  type        = string
  default     = "kimai"
}

variable "kimai_db_user" {
  description = "Kimai database user"
  type        = string
  default     = "kimaiuser"
}

variable "kimai_db_password" {
  description = "Kimai database password"
  type        = string
  sensitive   = true
}

variable "kimai_app_secret" {
  description = "Kimai application secret"
  type        = string
  sensitive   = true
}

variable "kimai_trusted_hosts" {
  description = "Kimai trusted hosts"
  type        = string
  default     = "localhost|127.0.0.1"
}

variable "kimai_admin_email" {
  description = "Kimai administrator email"
  type        = string
}

variable "kimai_admin_password" {
  description = "Kimai administrator password"
  type        = string
  sensitive   = true
}
