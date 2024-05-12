import json
import boto3
import datetime

s3 = boto3.client('s3')

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
        
    s3_dump(final_jsonLog)
    
    return {
        'statusCode' : status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(final_jsonLog)
    }
    
# s3 to dump data as array of json    
def s3_dump(logBody):
    toByteStream = bytes(json.dumps(logBody).encode('UTF-8'))

    s3_bucket = 'ak-log-bucket1'
    
    ist_delta = datetime.timedelta(hours=5, minutes=30)
    utc_ist_combined_time = datetime.datetime.now() + ist_delta
    logTime = str(utc_ist_combined_time)
    fileType = 'arrayData'+'-'+f'{logTime}'+'.arraytype'
    
    
    s3.put_object(Bucket=s3_bucket, Key=fileType, Body=toByteStream )
    print("Dump Complete")
    
    
# s3 to dump data as json file
def s3_dump(logBody):
    toByteStream = bytes(json.dumps(logBody).encode('UTF-8'))

    s3_bucket = 'ak-log-bucket1'
    
    ist_delta = datetime.timedelta(hours=5, minutes=30)
    utc_ist_combined_time = datetime.datetime.now() + ist_delta
    logTime = str(utc_ist_combined_time)
    fileType = 'jsonData'+'-'+f'{logTime}'+'.json'
    
    
    s3.put_object(Bucket=s3_bucket, Key=fileType, Body=toByteStream )
    print("Dump Complete")
