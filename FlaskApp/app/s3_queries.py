from flask import Flask, jsonify
import json
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize the S3 client
s3_client = boto3.client('s3')
bucket_name = 'doojoo-user-data'


def create_user(name, email, password, age, gender, location):
    user = {}
    if get_user(email) != None:
        print("User with this email already exists")
        
    hashed_pword = generate_password_hash(password)
    user['name'] = name
    user['password'] = hashed_pword
    user['email'] = email
    user['age'] = age
    user['gender'] = gender
    user['location'] = location
    
    json_data = json.dumps(user)
    
    file_name = f"user_data_{email.replace('@', '_').replace('.', '_')}.json"
    
    try:
        s3_client.put_object(
            Body=json_data,
            Bucket=bucket_name,
            Key=file_name,
            ServerSideEncryption='AES256'  # Encrypt the file using S3's server-side encryption
        )
        print(f"User data stored successfully at {file_name}")
    except NoCredentialsError:
        print("No AWS credentials found.")
    except Exception as e:
        print(f"Error uploading to S3: {e}")
    
def get_user(email):
    """fetches user from s3 bucket, returns None if no match found"""
    pass

if __name__ == '__main__':
    create_user('lucas', 'lucas@gmail.com', 'password', '25', 'M', 'Santa Clara, CA')

