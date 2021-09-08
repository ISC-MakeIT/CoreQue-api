terraform {
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

# zipアーカイブを作成
data "archive_file" "lambda_scrape_function" {
  type = "zip"

  source_dir  = "${path.module}/lambda-scrape"
  output_path = "${path.module}/lambda-scrape.zip"

  # ビルドステップが完了するのを待つ
  depends_on = [
    null_resource.coreque_scrape_buildstep
  ]
}

# lambda関数の作成
resource "aws_lambda_function" "lambda_scrape_function" {
  function_name = "coreque_scrape"

  handler = "handler.lambda_handler"
  runtime = "python3.8"
  timeout = "30"

  filename         = data.archive_file.lambda_scrape_function.output_path
  source_code_hash = data.archive_file.lambda_scrape_function.output_base64sha256

  role = aws_iam_role.lambda_scrape_role.arn
}

# ビルドパイプラインの作成
resource "null_resource" "coreque_scrape_buildstep" {
  triggers = {
    handler     = base64sha256(file("lambda-scrape/handler.py"))
    requiremens = base64sha256(file("lambda-scrape/requirements.txt"))
    build       = base64sha256(file("lambda-scrape/build.sh"))
  }

  provisioner "local-exec" {
    command = "${path.module}/lambda-scrape/build.sh"
  }
}

# LambdaのIAMロールの作成
resource "aws_iam_role" "lambda_scrape_role" {
  name = "coreque_scrape"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

# LambdaのIAMロールのPolicyの作成
resource "aws_iam_role_policy" "lambda_scrape_role" {
  name = "coreque_scrape"
  role = aws_iam_role.lambda_scrape_role.id

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:BatchWriteItem",
          "dynamodb:BatchGetItem",
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket",
        ],
        "Resource" : "*"
      }
    ]
  })
}

# dynamodbの作成
resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "Meal"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Id"
  range_key      = "Classification"

  attribute {
    name = "Id"
    type = "S"
  }

  attribute {
    name = "Classification"
    type = "S"
  }

  attribute {
    name = "Name"
    type = "S"
  }

  attribute {
    name = "Calorie"
    type = "N"
  }

  attribute {
    name = "Carbohydrate"
    type = "N"
  }

  attribute {
    name = "Fat"
    type = "N"
  }

  attribute {
    name = "Protein"
    type = "N"
  }

  attribute {
    name = "Sodium"
    type = "N"
  }

  # ソートキーごとにLSIを設定
  local_secondary_index {
    name               = "CalorieIndex"
    range_key          = "Calorie"
    non_key_attributes = ["details"]
    projection_type    = "INCLUDE"
  }

  local_secondary_index {
    name               = "CarbohydrateIndex"
    range_key          = "Carbohydrate"
    non_key_attributes = ["details"]
    projection_type    = "INCLUDE"
  }

  local_secondary_index {
    name               = "FatIndex"
    range_key          = "Fat"
    non_key_attributes = ["details"]
    projection_type    = "INCLUDE"
  }

  local_secondary_index {
    name               = "ProteinIndex"
    range_key          = "Protein"
    non_key_attributes = ["details"]
    projection_type    = "INCLUDE"
  }

  local_secondary_index {
    name               = "SodiumIndex"
    range_key          = "Sodium"
    non_key_attributes = ["details"]
    projection_type    = "INCLUDE"
  }

  # 分類でグルーピングするためのインデックス
  global_secondary_index {
    name               = "MealClassifyIndex"
    hash_key           = "Classification"
    range_key          = "Name"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id"]
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

# 画像アップロード用のS3バケットの作成
resource "aws_s3_bucket" "b" {
  bucket = "meal-image-bucket"
  acl    = "public-read"

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    allowed_headers = ["*"]
    max_age_seconds = 3600
  }

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_policy" "b" {
  bucket = aws_s3_bucket.b.id

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "IPAllow",
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : "s3:GetObject",
        "Resource" : "arn:aws:s3:::${aws_s3_bucket.b.bucket}/*"
      }
    ]
  })
}