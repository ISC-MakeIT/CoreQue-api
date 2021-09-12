terraform {
  backend "remote" {
    organization = "MakeIT2021"
    workspaces {
      name = "kamicon2021"
    }
  }

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    archive = {
      source = "hashicorp/archive"
    }
    null = {
      source = "hashicorp/null"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
