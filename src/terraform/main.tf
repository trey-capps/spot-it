#GCP Cloud Storage Creation for Reddit-Spotify data
resource "google_storage_bucket" "spot-it-tf-bucket" {
  project       = var.gcp_project
  name          = var.gcp_bucket_name
  location      = var.gcp_region
  force_destroy = true
  storage_class = var.gcp_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }
}