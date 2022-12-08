provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "default" {
  account_id = var.service_account_name
  display_name = "Accounting WebApp Engine App"
}

resource "google_project_iam_binding" "sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.default.email}",
  ]
}

resource "google_project_iam_member" "gae_api" {
  project = var.project_id
  role    = "roles/compute.networkUser"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.default.email}"
}


resource "google_storage_bucket" "source_code" {
  name                        = "${var.app_engine_name}-source-code-location"
  storage_class               = "STANDARD"
  location                    = var.region
  uniform_bucket_level_access = false
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.root}/python"
  output_path = "${path.root}/zip_to_app_engine.zip"
  excludes    = [".idea", ".pytest_cache", "tests", ".env", ".help.txt"]
}

resource "google_storage_bucket_object" "zip" {
  name   = "source-code-for-${var.app_engine_name}.zip"
  bucket = google_storage_bucket.source_code.name
  source = data.archive_file.source.output_path
}

#resource "google_app_engine_application" "app" {
#  project     = var.project_id
#  location_id = var.region
#}

resource "google_app_engine_standard_app_version" "myapp_v1" {
  version_id     = "v1"
  service        = var.app_engine_name
  runtime        = "python38"
  instance_class = "B2"

  entrypoint {
    shell = "gunicorn -b :$PORT main:app"
  }

  deployment {
    zip {
      source_url = "https://storage.googleapis.com/${google_storage_bucket.source_code.name}/${google_storage_bucket_object.zip.name}"
    }
  }

  env_variables = {
    DATABASE_PORT_N = data.google_secret_manager_secret_version.port.secret_data
    USER_PASSWORD = data.google_secret_manager_secret_version.db_user_password.secret_data
    USER_NAME = data.google_secret_manager_secret_version.db_user_name.secret_data
    DATABASE_NAME = data.google_secret_manager_secret_version.db_name.secret_data
    SERVER_HOST = data.google_secret_manager_secret_version.host.secret_data
    USER = data.google_secret_manager_secret_version.web_user.secret_data
    PASSWORD = data.google_secret_manager_secret_version.web_user_password.secret_data
    SECRET_KEY = data.google_secret_manager_secret_version.flask_key.secret_data
  }

  basic_scaling {
    max_instances = 1
  }

  delete_service_on_destroy = true
  service_account = google_service_account.default.email
}

data "google_secret_manager_secret_version" "port" {
  secret = var.secret_port
}

data "google_secret_manager_secret_version" "db_user_password" {
  secret = var.secret_db_password
}

data "google_secret_manager_secret_version" "db_user_name" {
  secret = var.secret_db_user
}

data "google_secret_manager_secret_version" "db_name" {
  secret = var.secret_database_name
}

data "google_secret_manager_secret_version" "host" {
  secret = var.secret_server
}

data "google_secret_manager_secret_version" "web_user" {
  secret = var.secret_web_user
}

data "google_secret_manager_secret_version" "web_user_password" {
  secret = var.secret_web_user_pword
}

data "google_secret_manager_secret_version" "flask_key" {
  secret = var.secret_flask_key
}