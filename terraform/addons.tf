# addons.tf

# Create a PostgresSQL database for the development app
resource "heroku_addon" "development-database" {
  app  = heroku_app.development.name
  plan = "heroku-postgresql:hobby-dev" # https://elements.heroku.com/addons/heroku-postgresql
}

# Create a PostgresSQL database for the staging app
resource "heroku_addon" "staging-database" {
  app  = heroku_app.staging.name
  plan = "heroku-postgresql:hobby-dev" # https://elements.heroku.com/addons/heroku-postgresql
}

# Create a PostgresSQL database for the production app
resource "heroku_addon" "production-database" {
  app  = heroku_app.production.name
  plan = "heroku-postgresql:hobby-dev" # https://elements.heroku.com/addons/heroku-postgresql
}
