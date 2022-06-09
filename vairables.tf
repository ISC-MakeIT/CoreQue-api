# Input variable definitions\

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "ap-northeast-1"
}

variable "environment" {
  description = "Environment name for all resources."

  type    = string
  default = "production"
}

variable "project_name" {
  description = "Project name for all resources."

  type    = string
  default = "kamicon2021"
}

variable "owner" {
  description = "Owner name for all resources."

  type    = string
  default = "masahiro-tajima"
}