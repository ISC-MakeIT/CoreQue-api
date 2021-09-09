# ビルドパイプラインの作成
resource "null_resource" "coreque_api_buildstep" {
  triggers = {
    handler      = base64sha256(file("lambda-api/handler.py"))
    requirements = base64sha256(file("lambda-api/requirements.txt"))
    build        = base64sha256(file("lambda-api/build.sh"))
  }

  provisioner "local-exec" {
    command = "${path.module}/lambda-api/build.sh"
  }
}

# zipアーカイブを作成
data "archive_file" "lambda_api_function" {
  type = "zip"

  source_dir  = "${path.module}/lambda-api"
  output_path = "${path.module}/lambda-api.zip"

  # ビルドステップが完了するのを待つ
  depends_on = [
    null_resource.coreque_api_buildstep
  ]
}

# lambdaのIAMロールを作成
resource "aws_iam_role" "lambda_api_role" {
  name = "coreque-api"

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

# LambdaのIAMロールにPolicyをattach
resource "aws_iam_role_policy_attachment" "lambda_api_policy" {
  role = aws_iam_role.lambda_api_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# lambda関数の作成
resource "aws_lambda_function" "lambda_api_function" {
  function_name = "coreque-api"

  handler = "handler.lambda_handler"
  runtime = "python3.8"
  timeout = "30"

  filename         = data.archive_file.lambda_api_function.output_path
  source_code_hash = data.archive_file.lambda_api_function.output_base64sha256

  role = aws_iam_role.lambda_api_role.arn
}

# API Gatewayの作成
resource "aws_api_gateway_rest_api" "example" {
  body = jsonencode({
    openapi = "3.0.1"
    info = {
      title   = "example"
      version = "1.0"
    }
    paths = {
      "/path1" = {
        get = {
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://ip-ranges.amazonaws.com/ip-ranges.json"
          }
        }
      }
    }
  })

  name = "example"
}

# bodyが変更されるたびデプロイする設定
resource "aws_api_gateway_deployment" "example" {
  rest_api_id = aws_api_gateway_rest_api.example.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.example.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# APIのスナップショット用のリソースを作成
resource "aws_api_gateway_stage" "example" {
  deployment_id = aws_api_gateway_deployment.example.id
  rest_api_id   = aws_api_gateway_rest_api.example.id
  stage_name    = "example"
}

