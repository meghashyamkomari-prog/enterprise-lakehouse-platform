variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "enterprise-lakehouse"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "dev"
}

variable "data_bucket_name" {
  description = "S3 bucket for data lake"
  type        = string
  default     = "enterprise-lakehouse-data-dev"
}
