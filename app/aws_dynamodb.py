import boto3

dynamodb = boto3.resource('dynamodb')

def create_users_table():
    table = dynamodb.create_table(
        TableName='subscribers',
        KeySchema=[
            {'AttributeName': 'email', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'email', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    table.wait_until_exists()
    print(f"Table {table.table_name} created successfully.")

def add_user(email: str, topics: list):
    table = dynamodb.Table('subscribers')
    response = table.put_item(
        Item={
            'email': email,
            'subscribed_topics': topics,
        }
    )
    print(f"User {email} added with topics: {topics}")

def update_user_topics(email: str, new_topics: list):
    table = dynamodb.Table('subscribers')
    response = table.update_item(
        Key={'email': email},
        UpdateExpression="SET subscribed_topics = :topics",
        ExpressionAttributeValues={':topics': new_topics},
        ReturnValues="UPDATED_NEW"
    )
    print(f"Updated topics for {email}: {response['Attributes']['subscribed_topics']}")

def get_all_users() -> list:
    table = dynamodb.Table('subscribers')
    response = table.scan()
    users = response['Items']
    return users

def get_user_by_email(email: str) -> dict:
    table = dynamodb.Table('subscribers')
    response = table.get_item(
        Key={'email': email}
    )
    if 'Item' in response:
        return response['Item']
    else:
        print(f"No user found with email: {email}")
        return None
    
def get_all_users_by_subject(subject: str) -> list:
    table = dynamodb.Table('subscribers')
    response = table.scan()
    users = response['Items']
    return [user for user in users if subject in user['subscribed_topics']]

def delete_user(email: str):
    table = dynamodb.Table('subscribers')
    response = table.delete_item(
        Key={'email': email}
    )
    print(f"Deleted user with email: {email}")

"""
def display_menu():
    print("\nChoose an option:")
    print("1. Add User")
    print("2. Update User Topics")
    print("3. Get All Users")
    print("4. Get User by Email")
    print("5. Get All Users by Subject")
    print("6. Delete User")
    print("7. Send Newsletter")
    print("8. Create Users Table")
    print("0. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            email = input("Enter email: ").strip()
            topics = input("Enter topics (comma-separated): ").strip().split(",")
            add_user(email, topics)
        elif choice == "2":
            email = input("Enter email: ").strip()
            topics = input("Enter new topics (comma-separated): ").strip().split(",")
            update_user_topics(email, topics)
        elif choice == "3":
            users = get_all_users()
            print(f"All users: {users}")
        elif choice == "4":
            email = input("Enter email: ").strip()
            user = get_user_by_email(email)
            if user:
                print(f"User: {user}")
        elif choice == "5":
            subject = input("Enter subject: ").strip()
            users = get_all_users_by_subject(subject)
            print(f"Users subscribed to {subject}: {users}")
        elif choice == "6":
            email = input("Enter email: ").strip()
            delete_user(email)
        elif choice == "7":
            subject = input("Enter newsletter subject: ").strip()
            body = input("Enter newsletter body: ").strip()
            subject_filter = input("Send to users subscribed to (subject): ").strip()
            subscribers = get_all_users_by_subject(subject_filter)
            send_newsletter(subject, body, subscribers)
        elif choice == "8":
            create_users_table()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

"""