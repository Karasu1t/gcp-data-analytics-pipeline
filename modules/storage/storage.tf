# Storage
resource "google_storage_bucket" "noetl-data" {
  name          = "${var.environment}-${var.project}-noetl-data"
  location      = "ASIA-NORTHEAST1"
  force_destroy = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 2
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_storage_bucket" "etl-data" {
  name          = "${var.environment}-${var.project}-etl-data"
  location      = "ASIA-NORTHEAST1"
  force_destroy = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 2
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
