import boto3
from AWS_Creds import *

loginTableName = 'login'
musicTableName = 'music'
usersJSONPath = 'users.json'
musicJSONPath = 'a1.json'


def createUser(newUser):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.Table(loginTableName)
    table.put_item(Item=newUser)
    print(f"User added for email: {newUser['email']}")


def userExists(userEmail):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.Table(loginTableName)
    response = table.get_item(
        Key={
            'email': userEmail
        }
    )
    return 'Item' in response


def verifyUser(userEmail, userPassword):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.Table(loginTableName)
    response = table.get_item(
        Key={
            'email': userEmail
        }
    )
    if 'Item' in response:
        return response['Item']['password'] == userPassword
    return False


def getUserName(userEmail):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )

    table = dynamodb.Table(loginTableName)
    response = table.get_item(
        Key={
            'email': userEmail
        }
    )
    if 'Item' in response:
        return response['Item']['username']
    return None
