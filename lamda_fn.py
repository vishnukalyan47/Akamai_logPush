import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

log_path = '/aklogs'
test_path = '/apistatus'

def lambda_handler(event, context):
    print('Request event: ', event)
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'POST' and path == log_path:
            response = kibana_call(json.loads(event['body']))
        elif http_method == 'GET' and path == test_path:
            response = "Test Vishnu"

    except Exception as e:
        print('Error:', e)
        response = {400, 'Error processing request'}

    return response

# Print Response, can add Kibana api here.
def kibana_call(request_body):
    try:
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return (200, body)
    
    except ClientError as e:
        print('Error:', e)
        return (400, e.response['Error']['Message'])
