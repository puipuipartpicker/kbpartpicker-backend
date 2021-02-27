# pipelines.tf

/*
    ** If transferring from user owned to new team pipeline, you must first transer ownership of
    pipeline in UI before couplings can be provisioned. Other way is to destroy pipeline and recreate it
    with organization added to heroku_app
*/

# Create a Heroku pipeline
resource "heroku_pipeline" "pipeline" {
  name = var.app_prefix
}

# Couple development app to api pipeline
resource "heroku_pipeline_coupling" "development" {
  app      = heroku_app.development.id
  pipeline = heroku_pipeline.pipeline.id
  stage    = "development"
}

# Couple staging app to api pipeline
resource "heroku_pipeline_coupling" "staging" {
  app      = heroku_app.staging.id
  pipeline = heroku_pipeline.pipeline.id
  stage    = "staging"
}

# Couple production app to api pipeline
resource "heroku_pipeline_coupling" "production" {
  app      = heroku_app.production.id
  pipeline = heroku_pipeline.pipeline.id
  stage    = "production"
}
