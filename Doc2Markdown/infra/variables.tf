variable "subscription_id" {
  description = "The Azure Subscription ID"
  type        = string
}

variable "client_id" {
  description = "The Azure Client ID"
  type        = string
}

variable "client_secret" {
  description = "The Azure Client Secret"
  type        = string
}

variable "tenant_id" {
  description = "The Azure Tenant ID"
  type        = string
}

variable "sqladmin_username" {
  description = "The SQL Server administrator username"
  type        = string
}

variable "sqladmin_password" {
  description = "The SQL Server administrator password"
  type        = string
  sensitive   = true
}
variable "secret_key" {
  description = "A secret key used in your application"
  type        = string
  sensitive   = true
}