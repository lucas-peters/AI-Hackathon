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

def create_user(name, email, password, age, gender, location) -> (bool):
    user = {}
    
    if get_user(email) != None:
        print("User with this email already exists")
        return False
        
    hashed_pword = generate_password_hash(password)
    user['name'] = name
    user['password'] = hashed_pword
    user['email'] = email
    user['age'] = age
    user['gender'] = gender
    user['location'] = location
    
    json_data = json.dumps(user)
    
    key_string = make_key_string(email)
    
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
    
def get_user(email):
    """fetches user from s3 bucket, returns None if no match found"""
    key_string = make_key_string(email)
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key_string)
    # handling NoSuchKey error. Tells us that this user has not been created yet
    except ClientError as e:
        return None
    
    return obj['Body'].read().decode('utf-8')
    
def get_password(email):
    return get_user['password']
    
    
# makes the key for the s3 bucket where we store the user data
def make_key_string(email):
    return f"{email.replace('@', '_').replace('.', '_')}.json"

if __name__ == '__main__':
    #create_user('lucas', 'lucas@gmail.com', 'password', '25', 'M', 'Santa Clara, CA')
    get_user('lucas@gmail.com')
    

# This is for us to upload locally
def upload_image(file_path: str):
    pass

# returns a specific image belonging to a user
def get_user_image(image_name: str):
    pass

# returns all images belonging to a user
def get_all_user_images():
    pass

