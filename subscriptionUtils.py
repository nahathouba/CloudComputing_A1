import boto3
import requests
from AWS_Creds import *

SUBSCRIPTION_TABLE_NAME = 'user-music-subscriptions'
MUSIC_TABLE_NAME = 'music'

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)


def createMusicSubscriptionTable():
    table = dynamodb.create_table(
        TableName=SUBSCRIPTION_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'user_email',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'music_title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_email',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'music_title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Music Subscription Table status:", table.table_status)


def addMusicSubscriptionS3(userEmail, musicTitle):
    table = dynamodb.Table(SUBSCRIPTION_TABLE_NAME)
    table.put_item(
        Item={
            'user_email': userEmail,
            'music_title': musicTitle
        }
    )
    isMusicSubscribed = musicSubcriptionExists(userEmail, musicTitle)
    return isMusicSubscribed


def getMusicSubscriptions(userEmail):
    url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/getMusicSubscription?email=' + \
        str(userEmail)

    response = requests.get(url)

    return response.json()


def musicSubcriptionExists(user_email, music_title):
    table = dynamodb.Table(SUBSCRIPTION_TABLE_NAME)
    response = table.get_item(
        Key={
            'user_email': user_email,
            'music_title': music_title
        }
    )
    return 'Item' in response


def removeMusicSubscriptionS3(userEmail, musicTitle):
    table = dynamodb.Table(SUBSCRIPTION_TABLE_NAME)
    table.delete_item(
        Key={
            'user_email': userEmail,
            'music_title': musicTitle
        }
    )
    isMusicStillSubscribed = musicSubcriptionExists(userEmail, musicTitle)
    return not isMusicStillSubscribed
