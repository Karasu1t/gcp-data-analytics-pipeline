# Storage
resource "google_storage_bucket" "etldata" {
  name          = "${var.environment}-${var.project}-etldata"
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

# Dataflow
resource "google_storage_bucket" "dataflow" {
  name          = "${var.environment}-${var.project}-dataflow"
  location      = "ASIA-NORTHEAST1"
  force_destroy = true
  uniform_bucket_level_access = true
}


# Storage Original data(Default)
resource "google_storage_bucket_object" "salary" {
  name   = "salary.zip"
  source = "../../data/salary.zip"
  bucket = google_storage_bucket.etldata.name

  depends_on = [google_storage_bucket.etldata]
}

resource "google_storage_bucket_object" "regularemployee" {
  name   = "regularemployee.zip"
  source = "../../data/regularemployee.zip"
  bucket = google_storage_bucket.etldata.name

  depends_on = [google_storage_bucket.etldata]
}

resource "google_storage_bucket_object" "nonregularemployee" {
  name   = "nonregularemployee.zip"
  source = "../../data/nonregularemployee.zip"
  bucket = google_storage_bucket.etldata.name

  depends_on = [google_storage_bucket.etldata]
}

resource "google_storage_bucket_object" "passengers" {
  name   = "passengers.zip"
  source = "../../data/passengers.zip"
  bucket = google_storage_bucket.etldata.name

  depends_on = [google_storage_bucket.etldata]
}