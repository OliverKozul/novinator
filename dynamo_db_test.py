import boto3
from mail_test import send_newsletter

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')

# Create the Users table
def create_users_table():
    table = dynamodb.create_table(
        TableName='subscribers',
        KeySchema=[
            {'AttributeName': 'email', 'KeyType': 'HASH'},  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'email', 'AttributeType': 'S'},  # String
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    table.wait_until_exists()
    print(f"Table {table.table_name} created successfully.")

def add_user(email, topics):
    table = dynamodb.Table('subscribers')
    response = table.put_item(
        Item={
            'email': email,
            'subscribed_topics': topics,
        }
    )
    print(f"User {email} added with topics: {topics}")

def update_user_topics(email, new_topics):
    table = dynamodb.Table('subscribers')
    response = table.update_item(
        Key={'email': email},
        UpdateExpression="SET subscribed_topics = :topics",
        ExpressionAttributeValues={':topics': new_topics},
        ReturnValues="UPDATED_NEW"
    )
    print(f"Updated topics for {email}: {response['Attributes']['subscribed_topics']}")

def get_user(email):
    table = dynamodb.Table('subscribers')
    response = table.get_item(
        Key={'email': email}
    )
    if 'Item' in response:
        return response['Item']
    else:
        print(f"No user found with email: {email}")
        return None
    
def get_all_users_by_subject(subject):
    table = dynamodb.Table('subscribers')
    response = table.scan()
    users = response['Items']
    return [user['email'] for user in users if subject in user['subscribed_topics']]

def delete_user(email):
    table = dynamodb.Table('subscribers')
    response = table.delete_item(
        Key={'email': email}
    )
    print(f"Deleted user with email: {email}")

# add_user("oliverkozul@gmail.com", ["Technology", "Sports"])
# add_user("olivernpe@gmail.com", ["Finance", "Sports"])
# add_user("oliverkozul@gmail.com", ["Technology", "Sports"])

# update_user_topics("oli4@gmail.com", ["Finance"])

# print(get_user("oli@gmail.com")["subscribed_topics"])

# print(get_all_users_by_subject("Technology"))

# delete_user("oli@gmail.com")

send_newsletter(
    subject="Welcome to Our Newsletter",
    body="Thank you for subscribing to our newsletter!",
    subscribers=get_all_users_by_subject("Finance")
)

# create_users_table()


