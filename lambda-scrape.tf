# lambda関数の作成
resource "aws_lambda_function" "lambda_scrape_function" {
  function_name = "coreque_scrape"

  handler = "handler.lambda_handler"
  runtime = "python3.8"
  timeout = "600"

  filename         = data.archive_file.lambda_scrape_function.output_path
  source_code_hash = data.archive_file.lambda_scrape_function.output_base64sha256

  role = aws_iam_role.lambda_scrape_role.arn
}

# zipアーカイブを作成
data "archive_file" "lambda_scrape_function" {
  type = "zip"

  source_dir  = "${path.module}/lambda-scrape"
  output_path = "${path.module}/lambda-scrape.zip"
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

# スケジュールの作成
resource "aws_cloudwatch_event_rule" "everyday" {
  name                = "coreque_scrape_everyday"
  description         = "Fires everyday"
  schedule_expression = "cron(0 10 * * ? *)"
}

# イベントトリガーの作成
resource "aws_cloudwatch_event_target" "everyday" {
  target_id = "coreque_scrape"
  rule      = aws_cloudwatch_event_rule.everyday.name
  arn       = aws_lambda_function.lambda_scrape_function.arn
}

# lambdaの起動許可を与える
resource "aws_lambda_permission" "lambda_scrape_call_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_scrape_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.everyday.arn
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
    name = "Status"
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
    name = "Fibre"
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
    name               = "FibreIndex"
    range_key          = "Fibre"
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

  global_secondary_index {
    name               = "StatusCalorieGSI"
    hash_key           = "Status"
    range_key          = "Calorie"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Classification", "Name"]
  }

  global_secondary_index {
    name               = "StatusProteinGSI"
    hash_key           = "Status"
    range_key          = "Protein"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Classification", "Name"]
  }

  global_secondary_index {
    name               = "StatusFatGSI"
    hash_key           = "Status"
    range_key          = "Fat"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Classification", "Name"]
  }

  global_secondary_index {
    name               = "StatusCarbohydrateGSI"
    hash_key           = "Status"
    range_key          = "Carbohydrate"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Classification", "Name"]
  }

  global_secondary_index {
    name               = "StatusFibreGSI"
    hash_key           = "Status"
    range_key          = "Fibre"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Classification", "Name"]
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
