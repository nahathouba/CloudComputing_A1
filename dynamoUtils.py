import requests


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
    # Lambda function API Gateway address to verify user
    url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/verifyUser'
    user = {'email': userEmail, 'password': userPassword}
    response = requests.post(url, json=user)

    if response.status_code == 200:
        return True

    return False


def getUserName(userEmail):
    # Lambda function API Gateway address to get user name
    url = 'https://44lyi97043.execute-api.us-east-1.amazonaws.com/default/getUserName'
    params = {'email': userEmail}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return None
