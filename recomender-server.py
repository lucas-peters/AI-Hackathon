from flask import Flask, jsonify, request

# Create a Flask app instance
app = Flask(__name__)

import boto3
import json

access_key = "AKIA3G3YSRMR7BGQ4WVG"
secret_key = "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"

# Initialize AWS clients
s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,

    region_name="us-west-2",
)

bedrock = boto3.client(
    service_name="bedrock-runtime",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,

    region_name="us-west-2",
)

def fetch_image_urls(bucket_name, image_path):
    """
    Fetch all image URLs from the specified S3 bucket and path.

    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - image_path (str): The path to the folder containing the images.

    Returns:
    - list: A list of full image URLs.
    """
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=image_path)
    image_urls = []

    for obj in response.get("Contents", []):
        if obj["Key"].endswith((".jpg", ".jpeg", ".png")):  # Process only image files
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{obj['Key']}"
            image_urls.append(image_url)
   
    print(f"Fetched {len(image_urls)} image URLs.")
    return image_urls

# Fetch wardrobe metadata from S3
def fetch_user_metadata(bucket_name, user_path) -> json:
    """Fetch all wardrobe metadata JSON files from S3."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=user_path)
    wardrobe_metadata = []
    # wardrobe_metadata = dict()

    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".json"):  # Process only JSON files
            file_obj = s3.get_object(Bucket=bucket_name, Key=obj["Key"])
            metadata = json.loads(file_obj["Body"].read().decode("utf-8"))
            metadata["filename"] = f"https://{bucket_name}.s3.amazonaws.com/{obj['Key'].replace('metadata', 'images')[:-5]}"
            
            wardrobe_metadata.append(metadata)
            
    
    print(f"Fetched {len(wardrobe_metadata)} wardrobe items.")
    return wardrobe_metadata

# Filter metadata based on context
def filter_wardrobe_metadata(wardrobe_metadata, context) -> list:
    """Filter wardrobe items based on occasion and season."""
    occasion = context.args.get("occasion", "").lower()
    season = context.args.get("season", "").lower()

    # filtered_items = [
    #     item for item in wardrobe_metadata
    #     if occasion in [o.lower() for o in item.get("suitable_occasions", [])]
    #     and season in [s.lower() for s in item.get("season", [])]
    # ]
    filtered_items = [item for item in wardrobe_metadata]
    # filtered_items = [(key, value) for key, value in wardrobe_metadata.items() ]
    print(filtered_items)
    print("\n")
    print(f"Filtered {len(filtered_items)} items matching the context.")
    return filtered_items

# Generate recommendations using Llama 3.2
def recommend_clothes(context, filtered_metadata, image_urls) -> json:
    """Generate clothing recommendations using Llama 3.2."""
    prompt = f"""
    Based on the following inputs, please recommend suitable clothing items:

            Occasion: {context.args.get('occasion', 'unknown')}
            Season: {context.args.get('season', 'unknown')}

            Wardrobe Metadata:
            {json.dumps(filtered_metadata)}
            
            In only amoung the above data about warddrobe 
            
            
            Please pick one top wear(shirt, tops, etc), one bottom wear(pants, skirts, etc) and one footwear (shoes, high heels, etc) and
            respond in JSON format with the following fields and nothing else!:            
            - reason: (a brief explanation of why this item is recommended)
            - filename: if you picked an item, get the "filename" value of that item
            
            If there are no apropriate clothes, reply with a null or none value.
            
                        
    """
    
    model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

    request_body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    
    response = bedrock.invoke_model(
        modelId=model_id,
        body=request_body
    )

    print(response)

    response_body = json.loads(response["body"].read().decode("utf-8"))
    # return json.dumps({"outputText": response_body})
    # print(type(response_body))
    # print(response_body)
    # print("\n\n\n\n\n\n")
    # # return response_body
    return json.loads(response_body['content'][0]['text'])



    # return response

# Lambda handler
def lambda_handler(context) -> json:
    # Example user input
    # user_input = event["user_input"]
    bucket_name = "doojoo-clothes-data"
    user_path = "users/test_user_123/metadata/"
    image_path = "users/test_user_123/images/"
    
    try:        
        # context = {
        #     "occasion": "going to a comic-con",
        #     "season": "unknown"
        # }

        # Step 2: Fetch wardrobe metadata from S3
        wardrobe_metadata = fetch_user_metadata(bucket_name, user_path)

        # Step 3: Filter metadata based on context
        filtered_metadata = filter_wardrobe_metadata(wardrobe_metadata, context)

        image_urls = fetch_image_urls(bucket_name, image_path)

        # Step 4: Generate recommendations using Llama 3.2
        recommendations = recommend_clothes(context, filtered_metadata, image_urls)

        

        return {
            "statusCode": 200,
            "body": recommendations
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Define a route for a GET request
@app.route('/get', methods=['GET'])
def greet():

    """Request coming in:
    {
        occation,
        location,
        time_data,
        season,
        userID
    }
    """
    # event = {
    #     "user_input": "I need something for a casual wear in the winter.",
    #     "s3_url": "s3://doojoo-clothes-data/users/test_user_123/metadata/"
    # }
    # bucket_url = f"s3://doojoo-clothes-data/users/{request.args.get("userID")}/metadata/"
    # event = dict()
    # event["user_input"] = request.args.get("user_input")
    # event["s3_url"] = request.args.get(bucket_url)
    # context = None  # You can mock context if needed
    response = lambda_handler(request)

    return jsonify(response)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
