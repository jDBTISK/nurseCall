terraform {
  required_version = ">= 0.14.7"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # version 3系の最新版を指定
      version = "~> 3.0"
    }
  }
}
