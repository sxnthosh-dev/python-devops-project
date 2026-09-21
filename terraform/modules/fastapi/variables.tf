variable "image" {
  description = "FastAPI Docker image"
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
