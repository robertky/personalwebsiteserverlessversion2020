import json
import os

import boto3
from decimal import Decimal

print('Loading function')
region_name = os.environ['REGION_NAME']
table_name = os.environ['TABLE_NAME']


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return '`' + str(o) + '`'  # ` is special, will be removed later
        return super(DecimalEncoder, self).default(o)

#Response structure.
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res, cls=DecimalEncoder).replace("\"`", '').replace("`\"", ''),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def update_count():
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    #If count item exists in table, do this.
    try:
        response = table.update_item(
            Key={
                'VisitorID': 'VisitorCount'
            },
            UpdateExpression="set CountTracker=CountTracker + :r",
            ExpressionAttributeValues={
                ':r': Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    #If table is created, but no item exists yet, do this. Create the first item.
    except:
        table.put_item(TableName=table_name, Item={'VisitorID': 'VisitorCount', 'CountTracker': Decimal(1)})
        response = table.get_item(Key={'VisitorID': 'VisitorCount'})
        return response


def lambda_handler(event, context):
    counterResponse = {}
    counterResponse['Count'] = update_count()

    # return counterResponse
    return respond(None, res=counterResponse)
