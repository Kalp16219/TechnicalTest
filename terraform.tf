provider "aws" {
  region = "us-east-1"
}

# S3 Bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "mybucket"
  acl    = "private"
}

# RDS Instance
resource "aws_db_instance" "my_instance" {
  identifier             = "myrdsinstance"  
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "mysql"
  engine_version         = "8.0.25"
  instance_class         = "db.t2.micro"
  name                   = "my_database"  
  username               = "admin"  
  password               = "abcd@123"  
  publicly_accessible    = false
}

# Glue Database
resource "aws_glue_catalog_database" "gluedatabase" {
  name = "gluedatabase"  
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for Lambda Execution
resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_execution_policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogGroup"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach Lambda Policy to Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_policy.arn
  role       = aws_iam_role.lambda_role.name
}
