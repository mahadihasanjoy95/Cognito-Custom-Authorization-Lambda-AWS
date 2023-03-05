from wsgiref import headers

import boto3
import os
import json
import uuid
from datetime import datetime

client = boto3.client('cognito-idp')

CognitoUserPool = os.getenv('CongnitoPoolId')


def lambda_handler(message, context):
    print("COGNITO POOL ID:::::::: ", os.getenv('CongnitoPoolId'))
    if ('body' not in message or
            message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    table_name = os.environ.get('TABLE', 'water-billing-new')
    region = os.environ.get('REGION', 'ap-northeast-1')
    item_table = boto3.resource(
        'dynamodb',
        region_name=region
    )

    table = item_table.Table(table_name)
    user = json.loads(message['body'])
    randomString = str(uuid.uuid4())
    params = {
        'PK': "USER#",
        'SK': "USER#" + randomString,
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'isActive': user['isActive'],
        'email': user['email'],
        'phoneNumber': user['phoneNumber'],
        'createdAt': str(datetime.timestamp(datetime.now())),
        "GSI1PK": "USER#" + randomString,
        "GSI1SK": "USER#"
    }

    dbResponse = table.put_item(
        TableName=table_name,
        Item=params
    )
    # response = client.sign_up(
    #     ClientId=CognitoUserPool,
    #     Username=user['email'],
    #     Password=user['password'],
    # )

    response1 = client.admin_create_user(
        UserPoolId=CognitoUserPool,
        Username=user['email'],
        MessageAction='SUPPRESS',
    )

    print("RESPONSE 1:::: ", response1)
    response2 = client.admin_set_user_password(
        UserPoolId=CognitoUserPool,
        Username=user['email'],
        Password=user['password'],
        Permanent=True
    )

    reply1 = client.create_group(UserPoolId=CognitoUserPool, GroupName=user['role'])
    print("REPLY 1:::: ", reply1)
    reply2 = client.admin_add_user_to_group(UserPoolId=CognitoUserPool, Username=user['email'], GroupName=user['role'])
    print("Reply 2::::: ", reply2)
    print("RESPONSE 2:::: ", response2)
    return {
        "statusCode": 200,
        "headers": {},
        'body': json.dumps(response1, indent=4, sort_keys=True, default=str),  # default=decimal_default),
    }
