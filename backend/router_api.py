import json
import boto3
import os

sfn = boto3.client('stepfunctions')
STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']

def lambda_handler(event, context):
    # Log the event so you can see it in CloudWatch if it fails
    print(f"Received event: {json.dumps(event)}")

    # 1. Improved CORS Preflight check
    # HTTP APIs use 'routeKey' or 'requestContext.http.method'
    method = event.get('requestContext', {}).get('http', {}).get('method', 'UNKNOWN')
    
    if method == 'OPTIONS':
        return get_cors_response(200, "OK")

    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')

        if action == "start":
            topic = body.get('topic')
            response = sfn.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps({"topic": topic})
            )
            return get_cors_response(200, {"executionArn": response['executionArn'], "status": "RUNNING"})

        elif action == "status":
            execution_arn = body.get('executionArn')
            response = sfn.describe_execution(executionArn=execution_arn)
            status = response['status']
            
            if status == 'SUCCEEDED':
                output = json.loads(response['output'])
                return get_cors_response(200, {"status": status, "final_report": output.get('final_report')})
            else:
                return get_cors_response(200, {"status": status})
                
        return get_cors_response(400, {"error": "Invalid action"})

    except Exception as e:
        print(f"Error: {e}")
        return get_cors_response(500, {"error": str(e)})

def get_cors_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body_dict)
    }