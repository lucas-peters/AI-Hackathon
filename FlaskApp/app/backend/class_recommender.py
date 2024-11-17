
import boto3
import json





class RecommenderClass():
    def __init__(self):
        

        # Initialize AWS clients
        self.s3 = boto3.client(
            "s3",           

            region_name="us-west-2",
        )

        self.bedrock = boto3.client(
            service_name="bedrock-runtime",          

            region_name="us-west-2",
        )
    
    def fetch_user_metadata(self,bucket_name, user_path) -> json:
        """Fetch all wardrobe metadata JSON files from S3."""
        response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=user_path)
        wardrobe_metadata = []
        # wardrobe_metadata = dict()

        for obj in response.get("Contents", []):
            if obj["Key"].endswith(".json"):  # Process only JSON files
                file_obj = self.s3.get_object(Bucket=bucket_name, Key=obj["Key"])
                metadata = json.loads(file_obj["Body"].read().decode("utf-8"))
                metadata["filename"] = f"https://{bucket_name}.s3.amazonaws.com/{obj['Key'].replace('metadata', 'images')[:-5]}"
                
                wardrobe_metadata.append(metadata)
                
        
        # print(f"Fetched {len(wardrobe_metadata)} wardrobe items.")
        return wardrobe_metadata
    
    def filter_wardrobe_metadata(self,wardrobe_metadata, context:dict) -> list:
        """Filter wardrobe items based on occasion and season."""
        # occasion = context.get("occasion", "").lower()
        # season = context.get("season", "").lower()

        # filtered_items = [
        #     item for item in wardrobe_metadata
        #     if occasion in [o.lower() for o in item.get("suitable_occasions", [])]
        #     and season in [s.lower() for s in item.get("season", [])]
        # ]
        filtered_items = [item for item in wardrobe_metadata]
        # filtered_items = [(key, value) for key, value in wardrobe_metadata.items() ]
        # print(filtered_items)
        # print("\n")
        # print(f"Filtered {len(filtered_items)} items matching the context.")
        return filtered_items
    
    def recommend_clothes(self,context: dict, filtered_metadata) -> json:
        """Generate clothing recommendations using Llama 3.2."""
        prompt = f"""
        A user is looking for help to choose an outfit based on the following inputs, please recommend suitable clothing items:

                Occasion: {context.get('occasion', 'unknown')}
                weather: {context.get('weather', 'unknown')}
                location: {context.get('location', 'unknown')}
                time: {context.get('time', 'none')}
                date: {context.get('date', 'unknown')}


                Wardrobe Metadata:
                {json.dumps(filtered_metadata)}
                
                Use only the above data about his/her wardrobe.                 
                
                Please pick one top wear(shirt, tops, etc), one bottom wear(pants, skirts, etc) and one footwear (shoes, high heels, etc) and
                respond in JSON format with the following fields and nothing else!:            
                - reason: (a brief explanation of why this item is recommended)
                - filename: if you picked an item, get the "filename" value of that item
               
                
                Strictly adhere to the json format and If the user does not have the appropriate attire for the occasion, return a null or none
                which lets the user know they need to buy new clothes
                
                            
        """
        
        model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

        request_body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "temperature": 0.9,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
        
        response = self.bedrock.invoke_model(
            modelId=model_id,
            body=request_body
        )

        # print(response)

        response_body = json.loads(response["body"].read().decode("utf-8"))
       
        return json.loads(response_body['content'][0]['text'])
    
    def lambda_handler(self,context:dict) -> json:
        # Example user input
        # user_input = event["user_input"]
        bucket_name = "doojoo-clothes-data"
        user_path = f"users/{context.get('user_id')}/metadata/"
        
        
        try:        
            
            # Step 2: Fetch wardrobe metadata from S3
            wardrobe_metadata = self.fetch_user_metadata(bucket_name, user_path)
    
            # Step 3: Filter metadata based on context
            # filtered_metadata = self.filter_wardrobe_metadata(wardrobe_metadata, context)
            

            # Step 4: Generate recommendations using Llama 3.2
            # recommendations = self.recommend_clothes(context, filtered_metadata)
            recommendations = self.recommend_clothes(context.get("processed_data"), wardrobe_metadata)
            

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



# context = {'user_id': 'test_user_123', 'prompt': 'Going to a beach party in Miami tomorrow afternoon', 'processed_data': {'time': 'afternoon', 'date': 'tomorrow', 'location': 'Miami', 'occasion': 'beach party', 'weather': 'warm and sunny', 'additional_data': 'Beach party attire like swimwear, cover-ups, sandals, sunglasses, and sun protection would be appropriate.'}}
# context = {'user_id': 'test_user_123', 'prompt': 'Going to a diwali function', 'processed_data': {'time': 'afternoon', 'date': 'tomorrow', 'location': 'california', 'occasion': 'Indian-festival diwali', 'weather': 'warm evening', 'additional_data': ''}}
# context = {'user_id': 'test_user_123', 'prompt': 'Going to space', 'processed_data': {'time': 'day', 'date': 'in 10 days', 'location': 'space', 'occasion': 'flying to space', 'weather': 'space harsh cold', 'additional_data': ''}}
# rc = RecommenderClass()
# print(rc.lambda_handler(context))
        
