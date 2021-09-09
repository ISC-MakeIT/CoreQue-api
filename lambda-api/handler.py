import sys
sys.path.insert(0, "package/")
import boto3

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }