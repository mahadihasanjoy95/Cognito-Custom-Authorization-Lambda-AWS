import json


def lambda_handler(message, context):
    print("hi::::::::::::::::")
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 's3 Triggered!!!'})
    }
