import boto3
import hashlib
import time
from botocore.exceptions import ClientError, NoCredentialsError

def generate_filename(subject: str) -> str:
    # Convert subject to lowercase, replace spaces with dashes
    sanitized_subject = subject.lower().replace(" ", "-")
    # Generate SHA1 hash of the current time
    sha1_hash = hashlib.sha1(str(time.time()).encode()).hexdigest()[:8]
    # Combine the sanitized subject with the hash
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
        
def send_email_via_ses(subject: str, body: str, to_email: str):
    # AWS SES configuration
    sender_email = "no-reply@blokada.info"  # Must be verified in SES
    S3_BUCKET = "novinomator-email-archive"

    # Create a new SES client
    ses_client = boto3.client("ses")

    # Email content
    email_body = f"""
    Subject: {subject}

    {body}
    """

    # Try to send the email
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                "ToAddresses": [to_email],  # Recipient's email
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body}
                },
            }
        )
        print(f"Email sent successfully: {response}")
        upload_email_to_s3(S3_BUCKET, generate_filename(subject), body)
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")

def send_newsletter(subject: str, body: str, subscribers: list):
    for subscriber in subscribers:
        send_email_via_ses(subject, body, subscriber)

# Example usage
# send_email_via_ses(
#     subject="Welcome to Our Newsletter",
#     body="Thank you for subscribing to our newsletter!",
#     to_email="oliverkozul@gmail.com"
# )
