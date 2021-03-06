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

# zipアーカイブを作成
data "archive_file" "lambda_api_function" {
  type = "zip"

  source_dir  = "${path.module}/lambda-api"
  output_path = "${path.module}/lambda-api.zip"
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

# LambdaのIAMロールのPolicyを作成
resource "aws_iam_role_policy" "lambda_api_role" {
  name = "coreque-api"
  role = aws_iam_role.lambda_api_role.id

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:BatchGetItem",
          "dynamodb:GetObject",
          "dynamodb:GetObjectTagging",
        ],
        "Resource" : "*"
      }
    ]
  })
}

# APIGatewayの作成
resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "serverless_lambda_gateway"
  protocol_type = "HTTP"
}

# ステージを定義
resource "aws_apigatewayv2_stage" "lambda_api" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  name        = "meal"
  auto_deploy = true
}

# APIGatewayとLambdaを統合
# integration_methodではPOSTを指定しないとなぜか Internal Server Error になる
resource "aws_apigatewayv2_integration" "lambda_api" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.lambda_api_function.invoke_arn
  integration_method = "POST"
}

# HTTPリクエストをAPIGatewayに送信
resource "aws_apigatewayv2_route" "lambda_api" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "GET /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_api.id}"
}

# APIGatewayにLambdaの起動許可を与える
resource "aws_lambda_permission" "lambda_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_api_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}
