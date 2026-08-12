terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

module "service" {
  source              = "./modules/service"
  name                = var.service_name
  cluster_arn         = var.cluster_arn
  task_definition_arn = var.task_definition_arn
  desired_count       = var.desired_count
  private_subnet_ids  = var.private_subnet_ids
  security_group_ids  = var.security_group_ids
  target_group_arn    = var.target_group_arn
}
