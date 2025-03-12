import os
import shutil
from docx import Document
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Facebook API credentials
access_token = 'EAAONhsmiQ2IBO12nGtNg1FDzug82C1CVGvRgD8mdHfljZAmQyvNIXzb9Ok8uC9oECrCyXKe3gukuAZB1wiH2A9jt7AxCCgap2N7BAQngLQvqtRh8aZC733sOVvIiyAdgQVNHJOt1UPBjIMt44IKAZBEVgjAduJUxwP11Vdb5ZAOsUN7O4QouXs47pxStFSwZDZD'
page_id = '617619251426823'
FacebookAdsApi.init(access_token=access_token)

def get_lowest_numbered_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.docx')]
    files.sort(key=lambda f: float(f.split('_')[0]))
    return files[0] if files else None

def post_to_facebook(content):
    url = f"https://graph.facebook.com/v22.0/{page_id}/feed"
    payload = {
        'message': content,
        'access_token': access_token
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Post was successful.")
    else:
        print(f"Failed to post: {response.status_code}, {response.text}")

def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def move_file(file_path, archive_directory):
    shutil.move(file_path, archive_directory)

def send_email_notification():
    sender_email = "automate.analyze@gmail.com"
    receiver_email = "automate.analyze@gmail.com"
    password = "Jacxvacc@8"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Content Folder Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hello,
    There are only two files left in the content folder. Please add more content.
    """
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def post_content():
    base_dir = "C:\\Development\\Portfolio\\SocialMedia_Automation\\Content"
    archive_dir = os.path.join(base_dir, 'archive')
    os.makedirs(archive_dir, exist_ok=True)
    
    file_name = get_lowest_numbered_file(base_dir)
    if file_name:
        file_path = os.path.join(base_dir, file_name)
        content = read_docx(file_path)
        post_to_facebook(content)
        move_file(file_path, archive_dir)

    remaining_files = [f for f in os.listdir(base_dir) if f.endswith('.docx')]
    if len(remaining_files) == 2:
        send_email_notification()

# Call the function to post content
post_content()
