# Output value definitions

output "lambda_scrape_function_name" {
  description = "Name of the Lambda Scrape function."

  value = aws_lambda_function.lambda_scrape_function.function_name
}
