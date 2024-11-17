from flask import Flask, jsonify
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from botocore.exceptions import *
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = 'doojoo-user-data'

def create_user(user: dict) -> (bool):
    
    if get_user(user['email']) != None:
        print("User with this email already exists")
        return False
        
    hashed_pword = generate_password_hash(user['password'])
    user['password'] = hashed_pword
    json_data = json.dumps(user)
    key_string = make_key_string(user['email'])
    
    try:
        s3_client.put_object(
            Body=json_data,
            Bucket=bucket,
            Key=key_string,
            ServerSideEncryption='AES256'  # Encrypt the file using S3's server-side encryption
        )
        print(f"User data stored successfully at {key_string}")
    except NoCredentialsError:
        print("No AWS credentials found.")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False
    return True
    
def get_user(email: str):
    """fetches user from s3 bucket, returns None if no match found"""
    key_string = make_key_string(email)
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key_string)
    # handling NoSuchKey error. Tells us that this user has not been created yet
    except ClientError as e:
        return None
    
    return obj['Body'].read().decode('utf-8')
    
def get_password(email: str):
    return get_user(email)['password']

def get_location(email: str):
    return get_user(email)['location']
    
    
# makes the key for the s3 bucket where we store the user data
def make_key_string(email):
    return f"{email.replace('@', '_').replace('.', '_')}.json"

if __name__ == '__main__':
    user = {'name' : 'Bob', 'email' :'bob@gmail.com', 'password' : 'password', 'age' : '69', 'gender': 'M', 'location': 'Timbuktu'}
    create_user(user)
    get_user('bob@gmail.com')
    

# This is for us to upload locally
def upload_image(file_path: str):
    pass

# returns a specific image belonging to a user
def get_user_image(image_name: str):
    pass

# returns all images belonging to a user
def get_all_user_images():
    pass

