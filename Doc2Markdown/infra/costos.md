# Informe de Costos de Infraestructura - Proyecto Doc2Markdown

## Recursos con Costo

| Recurso | Componente | Cantidad | Unidad | Costo |
|---------|------------|----------|--------|-------|
| azurerm_service_plan.doc2markdown_app_service_plan_jknew | Instance usage (B1) | 730 | hours | $12.41 |
| azurerm_mssql_database.doc2markdown_db_jknew | Compute (serverless, GP_S_Gen5_2) | *Variable* | vCore-hours | Depende del uso |
| azurerm_mssql_database.doc2markdown_db_jknew | Storage | 32 | GB | $3.68 |
| azurerm_mssql_database.doc2markdown_db_jknew | Long-term retention (LRS) | *Variable* | GB | Depende del uso |
| azurerm_mssql_database.doc2markdown_db_jknew | PITR backup storage (LRS) | *Variable* | GB | Depende del uso |

## Total: **16.09 USD/mes**

*Actualizado: 2025-04-28*
