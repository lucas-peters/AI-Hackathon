import boto3
import json
import requests
from datetime import datetime
from typing import Dict, Any, Tuple
from amazon_scraper import DoojooRecommendationSystem
from class_recommender import RecommenderClass

class PromptProcessor:
    def __init__(self):
        """Initialize AWS clients"""
        self.bedrock = boto3.client('bedrock-runtime')
    
    def create_analysis_prompt(self, user_prompt: str, current_data: Dict[str, Any]) -> str:
        """Create a structured prompt for Bedrock"""
        return f"""Extract event details from the following user prompt and current information, focusing on fashion-relevant context.

        User's prompt: "{user_prompt}"

        Current information:
        - Time: {current_data.get('time', 'NA')}
        - Date: {current_data.get('date', 'NA')}
        - Location: {current_data.get('location', 'NA')}

        Based on the above information, create a JSON object with these exact fields:
        {{
            "time": "<specific time of day or NA>",
            "date": "<specific date or NA>",
            "location": "<specific location or NA>",
            "occasion": "<specific event/occasion type>",
            "weather": "<deduct or assume expected weather conditions based on location, date and time>",
            "additional_data": "<any fashion-relevant context>"
        }}

        Prioritize information from the user's prompt over current information. If any field cannot be determined, use "NA".

        Return only the JSON object, no additional text."""

    def process_bedrock_response(self, response_text: str) -> Dict[str, Any]:
        """Process and validate Bedrock response"""
        try:
            # Extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            
            data = json.loads(response_text[start:end])
            
            # Validate required fields
            required_fields = ['time', 'date', 'location', 'occasion', 'weather', 'additional_data']
            return {field: data.get(field, 'NA') or 'NA' for field in required_fields}
            
        except Exception as e:
            print(f"Response processing error: {str(e)}")
            return {field: 'NA' for field in ['time', 'date', 'location', 'occasion', 'weather', 'additional_data']}

    def invoke_bedrock(self, prompt: str) -> Dict[str, Any]:
        """Invoke Bedrock with correct API parameters"""
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.1,
                "top_p": 0.9,
                "stop_sequences": ["\n\nHuman:", "\n\nAssistant:"]
            }
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response.get('body').read())
            return self.process_bedrock_response(response_body['content'][0]['text'])
            
        except Exception as e:
            print(f"Bedrock API error: {str(e)}")
            return {field: 'NA' for field in ['time', 'date', 'location', 'occasion', 'weather', 'additional_data']}

    def process_prompt(self, prompt: str, user_id: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user prompt and return structured data"""
        try:
            analysis_prompt = self.create_analysis_prompt(prompt, current_data)
            processed_data = self.invoke_bedrock(analysis_prompt)
            
            return {
                'user_id': user_id,
                'prompt': prompt,
                'processed_data': processed_data
            }
            
        except Exception as e:
            print(f"Processing error: {str(e)}")
            return {
                'user_id': user_id,
                'prompt': prompt,
                'processed_data': {
                    'time': 'NA',
                    'date': 'NA',
                    'location': 'NA',
                    'occasion': 'NA',
                    'weather': 'NA',
                    'additional_data': 'NA'
                }
            }

"""Lucas Call's this API"""
def process_flask_request(prompt: str, user_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming Flask requests"""
    #Pre-process the prompt to relevant information"""
    promptProcessor = PromptProcessor()
    data =  promptProcessor.process_prompt(prompt, user_id, input_data)
    #print(data)

    # Get recommendations from wardrobe
    recommender_from_wadrobe = RecommenderClass()
    wardrobe_recommendations = json.dumps(recommender_from_wadrobe.lambda_handler(data))
    buying_recommendations = json.dumps({})

    if prompt.strip():
        # Get recommendations to buy
        recommender_to_buy = DoojooRecommendationSystem()
        buying_recommendations = json.dumps(recommender_to_buy.get_recommendations(data), indent=2)
        #print(json.dumps(buying_recommendations, indent=2))

    return wardrobe_recommendations, buying_recommendations


"""Sample Test"""
if __name__ == "__main__":
    sample_prompt = "Going to a beach party in Miami tomorrow afternoon"
    sample_user_id = "test_user_123"
    sample_input_data = {
        "time": "NA",
        "date": "NA",
        "location": "NA"
    }
    
    result = process_flask_request(sample_prompt, sample_user_id, sample_input_data)
    print(json.dumps(result, indent=2))
