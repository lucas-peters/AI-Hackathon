
import boto3
import json

class RecommenderClass():
    def __init__(self):
        self.access_key = "AKIA3G3YSRMRWN3MRXD4"
        self.secret_key = "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"

        # Initialize AWS clients
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,

            region_name="us-west-2",
        )

        self.bedrock = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,

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
                
        
        print(f"Fetched {len(wardrobe_metadata)} wardrobe items.")
        return wardrobe_metadata
    
    def filter_wardrobe_metadata(self,wardrobe_metadata, context:dict) -> list:
        """Filter wardrobe items based on occasion and season."""
        occasion = context.get("occasion", "").lower()
        season = context.get("season", "").lower()

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
    
    def recommend_clothes(self,context: dict, filtered_metadata) -> json:
        """Generate clothing recommendations using Llama 3.2."""
        prompt = f"""
        Based on the following inputs, please recommend suitable clothing items:

                Occasion: {context.get('occasion', 'unknown')}
                Season: {context.get('season', 'unknown')}

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
        user_path = "users/test_user_123/metadata/"
        
        
        try:        
            
            # Step 2: Fetch wardrobe metadata from S3
            wardrobe_metadata = self.fetch_user_metadata(bucket_name, user_path)

            # Step 3: Filter metadata based on context
            filtered_metadata = self.filter_wardrobe_metadata(wardrobe_metadata, context)
            

            # Step 4: Generate recommendations using Llama 3.2
            recommendations = self.recommend_clothes(context, filtered_metadata)
            

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



context = {
    "occasion":"party",
    
    "season": "summer"
}
rc = RecommenderClass()
print(rc.lambda_handler(context))
        
