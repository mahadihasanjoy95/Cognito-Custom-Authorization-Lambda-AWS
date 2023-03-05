from wsgiref import headers

import boto3
import os
import json
from boto3.dynamodb.conditions import Key


def lambda_handler(message, context):
    if ('httpMethod' not in message or
            message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    # userId = message["queryStringParameters"]['userId']

    table_name = os.environ.get('TABLE', 'water-billing-new')
    region = os.environ.get('REGION', 'ap-northeast-1')

    item_table = boto3.resource(
        'dynamodb',
        region_name=region
    )

    table = item_table.Table(table_name)
    response = table.query(
            KeyConditionExpression=Key('PK').eq('USER#')
        )
    # return {
    #     'statusCode': 200,
    #     'headers': {},
    #     'body': json.dumps(response['Items'])
    # }
    return {
        "statusCode": 200,
        "headers": {},
        'body': json.dumps(response['Items'], indent=4, sort_keys=True, default=str),  # default=decimal_default),
    }
