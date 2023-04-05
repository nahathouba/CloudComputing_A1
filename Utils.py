import boto3
import json
import time

aws_access_key_id = "ASIASEPGD37DVWPOULRT"
aws_secret_access_key = "7CVojM0GYvHH/PKkS0NegBYPhCJZKsiakh4vJGBZ"
aws_session_token = "FwoGZXIvYXdzEDcaDJ28M8awHlMpi/7kUiLNAUJu8l522ivOnUKkNCPWVaIn1EmPg+aBgYGDwq/jcs8tjbsK2DD24o8Mu1I/4NNCGQZ4ns7hMvtgdUYr7hBWHOcTHYqmKLDYFIYYggDcH00Q/NISnWN0ViDTDNdbQr4CxMVXzvbvXeJQRPq5yU6YCoI8HYkgg8tO9DI9R5c7QDJDC1JUkqnRzQ/FZvoOY5WzNIlClgXCitwUbHE7iXd5zkE+EmHTiz/9qoHVXMj31MtkTKq3Gdf+xALBPCgQbA3O1rIxZSLpOhn7blYKHM8o/pK0oQYyLbBXKnBFBO0pGvxr2GEm2pE4UvTeImz/rJBiuzErBBsAKPts8TNI43Fl3jiEIA=="
region_name = "us-east-1"

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
