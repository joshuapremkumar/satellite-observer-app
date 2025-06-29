from appwrite.client import Client
from appwrite.services.account import Account

client = Client().set_endpoint("https://nyc.cloud.appwrite.io/v1").set_project("6861a98400361afe0a7d")
account = Account(client)

def login_user(email, password):
    try:
        session = account.create_email_session(email=email, password=password)
        return session
    except Exception as e:
        return None