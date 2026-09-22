variable "image" {
  description = "Kimai Docker image"
  type        = string
}

variable "db_host" {
  description = "MariaDB container hostname"
  type        = string
}

variable "db_port" {
  description = "MariaDB port"
  type        = string
  default     = "3306"
}

variable "db_name" {
  description = "Kimai database name"
  type        = string
}

variable "db_user" {
  description = "Kimai database user"
  type        = string
}

variable "db_password" {
  description = "Kimai database password"
  type        = string
  sensitive   = true
}

variable "network_name" {
  description = "Docker network name"
  type        = string
}

variable "app_secret" {
  description = "Kimai application secret"
  type        = string
  sensitive   = true
}

variable "trusted_hosts" {
  description = "Kimai trusted hosts"
  type        = string
  default     = "localhost|127.0.0.1"
}

variable "admin_email" {
  description = "Kimai administrator email"
  type        = string
}

variable "admin_password" {
  description = "Kimai administrator password"
  type        = string
  sensitive   = true
}
