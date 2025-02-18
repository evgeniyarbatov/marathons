terraform {
  backend "s3" {
    encrypt        = true
    bucket         = "arbatov-terraform-state"
    dynamodb_table = "arbatov-me-tf-state-lock"
    key            = "marathons-page.tfstate"
    region         = "ap-southeast-1"
  }
}