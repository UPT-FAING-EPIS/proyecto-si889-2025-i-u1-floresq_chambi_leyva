provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

# Grupo de recursos
resource "azurerm_resource_group" "doc2markdown_rg_jknew" {
  name     = "rgdoc2markdownjknew"
  location = "East US 2"
}

resource "azurerm_mssql_server" "doc2markdown_sql_server_jknew" {
  name                         = "newsqlserverdoc2markdownjknew"
  resource_group_name          = azurerm_resource_group.doc2markdown_rg_jknew.name
  location                     = "East US 2"
  version                      = "12.0"
  administrator_login          = var.sqladmin_username
  administrator_login_password = var.sqladmin_password

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_mssql_database" "doc2markdown_db_jknew" {
  name                        = "newdbdoc2markdownjknew"
  server_id                   = azurerm_mssql_server.doc2markdown_sql_server_jknew.id
  sku_name                    = "GP_S_Gen5_2"
  collation                   = "SQL_Latin1_General_CP1_CI_AS"
  auto_pause_delay_in_minutes = 60
  min_capacity                = 0.5
  storage_account_type        = "Local"
}

resource "azurerm_mssql_firewall_rule" "allow_azure_services_jknew" {
  name             = "AllowAzureServicesjknew"
  server_id        = azurerm_mssql_server.doc2markdown_sql_server_jknew.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_service_plan" "doc2markdown_app_service_plan_jknew" {
  name                = "newdoc2markdownappserviceplanjknew"
  location            = "East US 2"
  resource_group_name = azurerm_resource_group.doc2markdown_rg_jknew.name
  sku_name            = "B1"
  os_type             = "Linux"
}

resource "azurerm_app_service" "doc2markdown_app_service_jknew" {
  name                = "newdoc2markdownwebappjknew"
  location            = azurerm_resource_group.doc2markdown_rg_jknew.location
  resource_group_name = azurerm_resource_group.doc2markdown_rg_jknew.name
  app_service_plan_id = azurerm_service_plan.doc2markdown_app_service_plan_jknew.id

  app_settings = {
    "SQL_SERVER"     = azurerm_mssql_server.doc2markdown_sql_server_jknew.name
    "SQL_DATABASE"   = azurerm_mssql_database.doc2markdown_db_jknew.name
    "SQL_USERNAME"   = var.sqladmin_username
    "SQL_PASSWORD"   = var.sqladmin_password
    "SECRET_KEY"     = var.secret_key
  }

  site_config {
    linux_fx_version = "PYTHON|3.8"
  }

  connection_string {
    name  = "db_connection_string"
    value = "Server=tcp:${azurerm_mssql_server.doc2markdown_sql_server_jknew.name}.database.windows.net,1433;Database=${azurerm_mssql_database.doc2markdown_db_jknew.name};User ID=${var.sqladmin_username};Password=${var.sqladmin_password};Encrypt=true;TrustServerCertificate=false;"
    type  = "SQLAzure"
  }
}
