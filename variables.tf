variable "project_id" {
  type        = string
  description = "Name of the Google Project"
}

variable "region" {
  type        = string
  default     = "europe-west2"
  description = "Location for the resources"
}

variable "service_account_name" {
  type        = string
  description = "Name of the Service Account"
}

variable "app_engine_name" {
  type        = string
  description = "Name of the App Engine"
}

variable "secret_database_name" {
  type        = string
  description = "Keyword of secret database name"
}

variable "secret_port" {
  type        = string
  description = "Keyword of secret database port"
}

variable "secret_server" {
  type        = string
  description = "Keyword of secret database address"
}

variable "secret_db_user" {
  type        = string
  description = "Keyword of secret for database user name"
}

variable "secret_db_password" {
  type        = string
  description = "Keyword of secret for database user password"
}

variable "secret_flask_key" {
  type        = string
  description = "Keyword of secret for flask key"
}

variable "secret_web_user" {
  type        = string
  description = "Keyword of secret for user login"
}

variable "secret_web_user_pword" {
  type        = string
  description = "Keyword of secret for user login password"
}
