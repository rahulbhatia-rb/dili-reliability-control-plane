variable "aws_region" { type = string }
variable "service_name" { type = string }
variable "cluster_arn" { type = string }
variable "task_definition_arn" { type = string }
variable "desired_count" { type = number; default = 2 }
variable "private_subnet_ids" { type = list(string) }
variable "security_group_ids" { type = list(string) }
variable "target_group_arn" { type = string }
