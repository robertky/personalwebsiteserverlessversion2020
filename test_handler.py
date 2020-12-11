import os
import unittest
from unittest import TestCase, mock
from decimal import Decimal
import boto3
from moto import mock_dynamodb2


class TestDatabaseFunctions(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch.dict(os.environ, {"TABLE_NAME": "VisitorCountTable", "REGION_NAME": "us-east-1"})
    @mock_dynamodb2
    def test_table_updates(self):
        from lambda_handler import update_count
        dynamodb = boto3.client('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName="VisitorCountTable",
            KeySchema=[
                {
                    "AttributeName": "VisitorID",
                    "KeyType": "HASH"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "VisitorID",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        dynamodb.put_item(TableName='VisitorCountTable', Item={'VisitorID': {'S': 'VisitorCount'}, 'CountTracker': {'N': "1"}})
        response = update_count()
        self.assertEqual(Decimal('2'), response['Attributes']['CountTracker'])

    @mock.patch.dict(os.environ, {"TABLE_NAME": "VisitorCountTable", "REGION_NAME": "us-east-1"})
    @mock_dynamodb2
    def test_table_empty(self):
        from lambda_handler import update_count
        dynamodb = boto3.client('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName="VisitorCountTable",
            KeySchema=[
                {
                    "AttributeName": "VisitorID",
                    "KeyType": "HASH"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "VisitorID",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        response = update_count()
        self.assertEqual(Decimal('1'), response['Item']['CountTracker'])


if __name__ == '__main__':
    unittest.main()
