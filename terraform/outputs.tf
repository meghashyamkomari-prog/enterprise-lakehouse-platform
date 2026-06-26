output "raw_bucket_name" {
  description = "Raw layer S3 bucket name"
  value       = aws_s3_bucket.raw_layer.bucket
}

output "bronze_bucket_name" {
  description = "Bronze layer S3 bucket name"
  value       = aws_s3_bucket.bronze_layer.bucket
}

output "silver_bucket_name" {
  description = "Silver layer S3 bucket name"
  value       = aws_s3_bucket.silver_layer.bucket
}

output "gold_bucket_name" {
  description = "Gold layer S3 bucket name"
  value       = aws_s3_bucket.gold_layer.bucket
}

output "lakehouse_role_arn" {
  description = "IAM Role ARN"
  value       = aws_iam_role.lakehouse_role.arn
}
