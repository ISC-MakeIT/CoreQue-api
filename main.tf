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

