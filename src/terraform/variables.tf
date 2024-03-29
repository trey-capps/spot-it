#GCP authenticaiton file
variable "gcp_auth_file" {
  description = "GCP authenticaiton file"
}

# Define GCP project (ID)
variable "gcp_project" {
  description = "GCP Project ID"
}

#Define GCP storage bucket region
variable "gcp_region" {
  description = "Region for GCP resources"
  default     = "US-EAST1"
  type        = string
}

#Define GCP storage bucket name
variable "gcp_bucket_name" {
  description = "GCP bucket name"
  type        = string
}

#Define GCP storage class of the GCP storage bucket
variable "gcp_storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
}