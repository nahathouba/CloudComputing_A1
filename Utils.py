import boto3
import json
import time
from AWS_Creds import *

loginTableName = 'login'
musicTableName = 'music'
usersJSONPath = 'users.json'
musicJSONPath = 'a1.json'


def tableExists(tableName):
    dynamodbClient = boto3.client(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    tableNames = dynamodbClient.list_tables()['TableNames']
    return tableName in tableNames


def createLogInTable():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.create_table(
        TableName=loginTableName,
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("LogIn Table status:", table.table_status)

    # Load the users into the table
    putUsers(table)


def putUsers(table):
    istableExists = tableExists(loginTableName)
    if istableExists:
        # Wait for the table to be Activated
        time.sleep(10)

        with open(usersJSONPath) as file:
            users = json.load(file)

        for user in users:
            table.put_item(Item=user)
            print(f"User added for email: {user['email']}")


# Music Table Helpers

def loadMusic(table):
    istableExists = tableExists(musicTableName)
    if istableExists:
        # Wait for the table to be Activated
        time.sleep(10)

        with open(musicJSONPath) as file:
            musicData = json.load(file)

        for song in musicData['songs']:
            table.put_item(Item=song)
            print(f"Song added for title: {song['title']}")


def createMusicTable():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.create_table(
        TableName=musicTableName,
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Music Table status:", table.table_status)
    loadMusic(table)
