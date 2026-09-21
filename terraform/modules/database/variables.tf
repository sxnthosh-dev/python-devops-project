variable "db_root_password" {
  description = "MariaDB root password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "MariaDB database name"
  type        = string
}

variable "db_user" {
  description = "MariaDB application user"
  type        = string
}

variable "db_password" {
  description = "MariaDB application password"
  type        = string
  sensitive   = true
}

variable "network_name" {
  description = "Docker network name"
  type        = string
}
