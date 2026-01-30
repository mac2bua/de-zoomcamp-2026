terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.17.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json"
  project     = "my-project-id"
  region      = "us-central1"
}