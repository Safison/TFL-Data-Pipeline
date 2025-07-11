terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      ProjectName  = "TFL Data Pipeline"
      DeployedFrom = "Terraform"
      Repository   = "TFL_Data_Pipeline"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}