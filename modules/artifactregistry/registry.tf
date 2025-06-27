resource "google_artifact_registry_repository" "create_template" {
  provider      = google
  location      = var.gcp_region
  repository_id = "${var.environment}-${var.project}-create-template"
  format        = "DOCKER"
}
