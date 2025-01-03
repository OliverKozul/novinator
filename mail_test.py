import boto3
import hashlib
import time
from botocore.exceptions import ClientError, NoCredentialsError

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

def append_unsubscribe_link_html(body: str, email: str) -> str:
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    unsubscribe_url = f"https://pmf.blokada.info/unsubscribe_{email_hash}"
    unsubscribe_html = f'<p style="margin-top: 20px;">To unsubscribe, <a href="{unsubscribe_url}" target="_blank">click here</a>.</p>'

    return f"<div>{body}</div>{unsubscribe_html}"

def send_email_via_ses(subject: str, body: str, to_email: str):
    sender_email = "no-reply@blokada.info"
    ses_client = boto3.client("ses")
    email_body_with_unsubscribe_html = append_unsubscribe_link_html(body, to_email)

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                "ToAddresses": [to_email],
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Html": {"Data": email_body_with_unsubscribe_html}
                },
            }
        )
        print(f"Email sent to {to_email} successfully: {response}")
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")

def archive_email(subject: str, body: str):
    S3_BUCKET = "novinomator-email-archive"
    email_body_for_s3 = f"""
    Subject: {subject}

    {body}
    """
    upload_email_to_s3(S3_BUCKET, generate_filename(subject), email_body_for_s3)

def send_newsletter(subject: str, body: str, subscribers: list):
    archive_email(subject, body)
    for subscriber in subscribers:
        send_email_via_ses(subject, body, subscriber['email'])
