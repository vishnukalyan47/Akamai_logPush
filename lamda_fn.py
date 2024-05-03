import json
# from botocore.vendored import requests

log_path = '/aklogs'
status_test = '/apistatus'
test_path = '/test-path'

def lambda_handler(event, context):
    # print('Request event: ', event)
    test_bodyy = {"event ->":event}
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')
        if http_method == 'POST' and path == log_path:
            response = kibana_call(200, event['body'])
        elif http_method == 'GET' and path == test_path:
            response = getCalltest(200, test_bodyy)
        elif http_method == 'GET' and path == status_test:
            response = getCalltest(200,"Service is up and running - Vishnu")

    except Exception as e:
        print('Error->', e)
        response = {400, 'Error processing request'}

    return response

# Print Response, can add Kibana api here.
def getCalltest(status_code, request_body):
    return {
        'statusCode' : status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(request_body)
    }
    
def kibana_call(status_code, request_body):
    # json split logic ->
    rb_copy = request_body
    final_jsonLog = []
    start = 0
    while(start<len(rb_copy)):
        end = rb_copy.find('}', start) + 1
        if(end==0 or end ==-1):
            break
        individual_json_split = rb_copy[start:end]
        final_jsonLog.append(json.loads(individual_json_split))
        start = end
    
    
    return {
        'statusCode' : status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(final_jsonLog)
    }
