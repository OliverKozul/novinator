import boto3
import hashlib
import time
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import os

def generate_filename(subject: str) -> str:
    sanitized_subject = subject.lower().replace(" ", "-")
    sha1_hash = hashlib.sha1(str(time.time()).encode()).hexdigest()[:8]

    return f"{sanitized_subject}-{sha1_hash}.txt"

def upload_email_to_s3(bucket_name: str, key: str, email_body: str):
    s3_client = boto3.client("s3")

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=email_body,
            ContentType="text/plain"
        )
        print("Email uploaded successfully:", response)
    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print("An error occurred:", e)

def append_unsubscribe_link_html(body: str) -> str:
    unsubscribe_url = os.getenv('UNSUBSCRIBE_URL')
    unsubscribe_html = f'<p style="margin-top: 20px;">To unsubscribe, <a href="{unsubscribe_url}" target="_blank">click here</a>.</p>'

    return f"<div>{body}</div>{unsubscribe_html}"

def send_email_via_ses(subject: str, body: str, recipients: list):
    sender_email = os.getenv('SENDER_EMAIL')
    ses_client = boto3.client("ses")
    email_body_with_unsubscribe_html = append_unsubscribe_link_html(body)

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                "BccAddresses": recipients
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Html": {"Data": email_body_with_unsubscribe_html}
                },
            }
        )
        print(f"Email sent successfully: {response}")
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")

def archive_email(subject: str, body: str):
    S3_BUCKET = os.getenv('S3_BUCKET')
    email_body_for_s3 = f"""
    Subject: {subject}

    {body}
    """
    upload_email_to_s3(S3_BUCKET, generate_filename(subject), email_body_for_s3)

def send_newsletter(subject: str, body: str, subscribers: list):
    load_dotenv()
    subscriber_emails = [subscriber['email'] for subscriber in subscribers]
    archive_email(subject, body)
    send_email_via_ses(subject, body, subscriber_emails)
