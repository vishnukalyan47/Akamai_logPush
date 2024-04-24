import json
import requests

log_path = '/aklogs'
status_test = '/apistatus'
test_path = '/test-path'
url = "https://httpbin.org/post"

def lambda_handler(event, context):
    # print('Request event: ', event)
    test_bodyy = {"event":event}
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')
        if http_method == 'POST' and path == log_path:
            response = test_post(200, json.loads(event['body']))
        elif http_method == 'GET' and path == test_path:
            response = kibana_call(200, test_bodyy)
        elif http_method == 'GET' and path == status_test:
            response = kibana_call(200,"Service is up and running - Vishnu")

    except Exception as e:
        print('Error:', e)
        response = {400, 'Error processing request'}

    return response

# Print Response, can add Kibana api here.
def kibana_call(status_code, request_body):
    return {
        'statusCode' : status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(request_body)
    }
    
def test_post(status_code, request_body):
    response1 = requests.post(url, json=request_body)
    return {
        'statusCode' : response1.status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response1.json())
        
    }
