# Output value definitions

output "lambda_scrape_function_name" {
  description = "Name of the Lambda Scrape function."

  value = aws_lambda_function.lambda_scrape_function.function_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table."

  value = aws_dynamodb_table.basic-dynamodb-table.name
}

output "s3_bucket" {
  description = "Name of the S3 bucket."

  value = aws_s3_bucket.b.bucket
}

output "lambda_api_function_name" {
  description = "Name of the Lambda API function."

  value = aws_lambda_function.lambda_api_function.function_name
}

output "base_url" {
  description = "Base URL for API Gateway state."

  value = aws_apigatewayv2_stage.lambda_api.invoke_url
}
