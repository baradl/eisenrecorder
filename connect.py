import pymongo as pm
import requests


def connect_to_client():
    directory = "../"   
    with open(directory + "login_data.txt", "r") as login:
        mongodb_url = login.readlines()

    client = pm.MongoClient(mongodb_url)
    return client


def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False