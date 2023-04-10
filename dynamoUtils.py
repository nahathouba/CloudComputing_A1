import boto3
import requests
from AWS_Creds import *

loginTableName = 'login'
musicTableName = 'music'
usersJSONPath = 'users.json'
musicJSONPath = 'a1.json'


def createUser(newUser):
    # Create User Lambda function API endpoint
    url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/createUser'
    response = requests.post(url, json=newUser)
    if response.status_code == 200:
        return True

    return False


def userExists(userEmail):
    url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/userExists'
    params = {'email': userEmail}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return True

    return False


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
