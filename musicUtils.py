import boto3
from AWS_Creds import *

MUSIC_TABLE_NAME = 'music'

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)


def searchMusic(title=None, year=None, artist=None):
    musicTable = dynamodb.Table(MUSIC_TABLE_NAME)

    filterExpression = None

    if title:
        filterExpression = boto3.dynamodb.conditions.Attr('title').eq(title)

    if year:
        yearCondition = boto3.dynamodb.conditions.Attr('year').eq(year)
        if filterExpression:
            # If Title is provided, add year condition to it with ADD statement
            filterExpression = filterExpression & yearCondition
        else:
            filterExpression = yearCondition

    if artist:
        artistCondition = boto3.dynamodb.conditions.Attr('artist').eq(artist)
        if filterExpression:
            # If Title OR Year OR Both is provided, add artist condition to it with ADD statement
            filterExpression = filterExpression & artistCondition
        else:
            filterExpression = artistCondition

    if filterExpression:
        response = musicTable.scan(
            FilterExpression=filterExpression
        )
        availableMusic = response['Items']
    else:
        availableMusic = []

    return availableMusic
