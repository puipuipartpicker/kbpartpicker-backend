# variables.tf

variable "app_prefix" {
  description = "Prefix to be used in the naming of some of the created heroku resources"
  default     = "kbpartpicker-api"
}

variable "app_region" {
  description = "Region to be used for heroku resources"
  default     = "us" # switch to tokyo at a later time
}

variable "app_stack" {
  description = "Platform to run the application in"
  default     = "container"
}

#  If true, Hobby or above tier required for ACM
variable "app_acm" {
  description = "The flag representing Automated Certificate Management for the app"
  default     = false
}

variable "heroku_email" {
  description = "Email associated with your heroku account"
}

variable "heroku_api_key" {}
variable "DB_HOST" {}
variable "DB_DATABASE" {}
variable "DB_USERNAME" {}
variable "DB_PASSWORD" {}
variable "DEV_DB_HOST" {}
variable "DEV_DB_DATABASE" {}
variable "DEV_DB_USERNAME" {}
variable "DEV_DB_PASSWORD" {}
variable "STG_DB_HOST" {}
variable "STG_DB_DATABASE" {}
variable "STG_DB_USERNAME" {}
variable "STG_DB_PASSWORD" {}
variable "PRD_DB_HOST" {}
variable "PRD_DB_DATABASE" {}
variable "PRD_DB_USERNAME" {}
variable "PRD_DB_PASSWORD" {}
