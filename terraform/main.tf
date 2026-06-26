# S3 Buckets for Data Lakehouse
resource "aws_s3_bucket" "raw_layer" {
  bucket = "${var.project_name}-raw-${var.environment}"
  tags = {
    Name        = "Raw Data Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "raw"
  }
}

resource "aws_s3_bucket" "bronze_layer" {
  bucket = "${var.project_name}-bronze-${var.environment}"
  tags = {
    Name        = "Bronze Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "bronze"
  }
}

resource "aws_s3_bucket" "silver_layer" {
  bucket = "${var.project_name}-silver-${var.environment}"
  tags = {
    Name        = "Silver Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "silver"
  }
}

resource "aws_s3_bucket" "gold_layer" {
  bucket = "${var.project_name}-gold-${var.environment}"
  tags = {
    Name        = "Gold Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "gold"
  }
}

# Enable versioning on all buckets
resource "aws_s3_bucket_versioning" "raw" {
  bucket = aws_s3_bucket.raw_layer.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "bronze" {
  bucket = aws_s3_bucket.bronze_layer.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "silver" {
  bucket = aws_s3_bucket.silver_layer.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "gold" {
  bucket = aws_s3_bucket.gold_layer.id
  versioning_configuration {
    status = "Enabled"
  }
}

# IAM Role for Data Engineering
resource "aws_iam_role" "lakehouse_role" {
  name = "${var.project_name}-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  tags = {
    Name        = "Lakehouse IAM Role"
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM Policy for S3 Access
resource "aws_iam_policy" "lakehouse_s3_policy" {
  name        = "${var.project_name}-s3-policy-${var.environment}"
  description = "Policy for lakehouse S3 access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.raw_layer.arn,
          "${aws_s3_bucket.raw_layer.arn}/*",
          aws_s3_bucket.bronze_layer.arn,
          "${aws_s3_bucket.bronze_layer.arn}/*",
          aws_s3_bucket.silver_layer.arn,
          "${aws_s3_bucket.silver_layer.arn}/*",
          aws_s3_bucket.gold_layer.arn,
          "${aws_s3_bucket.gold_layer.arn}/*",
        ]
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lakehouse_attachment" {
  role       = aws_iam_role.lakehouse_role.name
  policy_arn = aws_iam_policy.lakehouse_s3_policy.arn
}
