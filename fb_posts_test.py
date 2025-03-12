import os
import shutil
from docx import Document
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
import requests

# Facebook API credentials
access_token = 'EAAONhsmiQ2IBO9VzcumnE20NzDeTc4e9ssdqFa5cZBASYjXr53Y2AvembXoLSepsYJbxke4m9GFtRnascFLHdr0l9pAvnOauGaAkWwXtm6eUt042WpOS5WMe4b6GEnB7U7ULcKAYaa8iYTxi8PcQllZBXzUGvCzJuPDuB9ZCM5D1iKaA6LdCEZCSgde7FuAP3M2uzqixrpvIAbVaNMt9YgZDZD'
page_id = '617619251426823'
FacebookAdsApi.init(access_token=access_token)

def get_lowest_numbered_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.docx')]
    files.sort(key=lambda f: int(f.split('_')[0]))
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

def post_content(day):
    base_dir = f"C:\\Users\\amymi\\OneDrive\\Automate and Analyze with Amy\\Development\\Portfolio\\SocialMedia_content_generator\\{day}s"
    archive_dir = os.path.join(base_dir, 'archive')
    os.makedirs(archive_dir, exist_ok=True)
    
    file_name = get_lowest_numbered_file(base_dir)
    if file_name:
        file_path = os.path.join(base_dir, file_name)
        content = read_docx(file_path)
        post_to_facebook(content)
        move_file(file_path, archive_dir)

# Test the process by calling post_content directly for Monday
post_content(day='Monday')
