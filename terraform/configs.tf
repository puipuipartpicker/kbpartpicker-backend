# configs.tf

# Common configs shared between all apps within pipeline
resource "heroku_config" "common" {
  #   vars = {
  #     NON_SENSATIVE_EXAMPLE_VAR = true
  #   }
}

resource "heroku_config" "dev" {
  sensitive_vars = {
    DB_HOST     = var.DEV_DB_HOST
    DB_USERNAME = var.DEV_DB_USERNAME
    DB_DATABASE = var.DEV_DB_DATABASE
    DB_PASSWORD = var.DEV_DB_PASSWORD
  }
}

resource "heroku_config" "stg" {
  sensitive_vars = {
    DB_HOST     = var.STG_DB_HOST
    DB_USERNAME = var.STG_DB_USERNAME
    DB_DATABASE = var.STG_DB_DATABASE
    DB_PASSWORD = var.STG_DB_PASSWORD
  }
}

resource "heroku_config" "prd" {
  sensitive_vars = {
    DB_HOST     = var.PRD_DB_HOST
    DB_USERNAME = var.PRD_DB_USERNAME
    DB_DATABASE = var.PRD_DB_DATABASE
    DB_PASSWORD = var.PRD_DB_PASSWORD
  }
}

# Associate development app with config vars
resource "heroku_app_config_association" "development" {
  app_id = heroku_app.development.id

  vars           = heroku_config.common.vars
  sensitive_vars = heroku_config.dev.sensitive_vars
}

# Associate staging app with config vars
resource "heroku_app_config_association" "staging" {
  app_id = heroku_app.staging.id

  vars           = heroku_config.common.vars
  sensitive_vars = heroku_config.stg.sensitive_vars
}

# Associate production app with config vars
resource "heroku_app_config_association" "production" {
  app_id = heroku_app.production.id

  vars           = heroku_config.common.vars
  sensitive_vars = heroku_config.prd.sensitive_vars
}
