resource "google_composer_environment" "composer_etl" {
  name   = "${var.environment}-${var.project}-composer-etl"
  region = var.gcp_region

  config {
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    software_config {
      image_version = "composer-3-airflow-2.10.5-build.6"
    }

    node_config {
      service_account = var.sa
    }
  }
}
