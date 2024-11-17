import boto3
from PIL import Image
import io
import json
import os

class ClothingImageProcessor:
    def __init__(self):
        # Initialize AWS clients
        self.bedrock = boto3.client('bedrock-runtime')
        self.s3 = boto3.client('s3')
        
    def process_image(self, image_path, user_id):
        """
        Main processing pipeline for clothing images
        """
        try:
            # 1. Load and prepare image
            with Image.open(image_path) as img:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=img.format)
                img_byte_arr = img_byte_arr.getvalue()
                
                import base64
                base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
            
            # 2. Extract basic image attributes using Bedrock Claude
            clothing_info = self._analyze_with_bedrock(base64_image)
            
            # 3. Enrich data with user preferences and occasions
            enriched_data = self._enrich_clothing_data(clothing_info, user_id)
            
            # 4. Store in S3
            self._store_in_s3(enriched_data, image_path, user_id)
            
            return enriched_data
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            raise

    def _analyze_with_bedrock(self, base64_image):
        """
        Use Bedrock's Claude model to analyze the clothing image
        """
        prompt = """
        Analyze this clothing image and provide the following information in JSON format:
        {
            "type": "the type of clothing item (e.g., shirt, pants, dress)",
            "color": "primary color of the item",
            "secondary_colors": ["list of secondary colors"],
            "pattern": "any patterns present",
            "style": "casual/formal/business/etc",
            "season": "appropriate seasons as a list",
            "material": "if identifiable",
            "gender_category": "menswear/womenswear/unisex",
            "gender_confidence": "high/medium/low (how confident are you about the gender categorization)",
            "fit_type": "regular/slim/loose/oversized",
            "specific_style": "streetwear/classic/bohemian/athletic/etc"
        }
        Consider design elements, cut, and styling to determine gender category. If the item appears gender-neutral or could be worn by any gender, categorize as 'unisex'. Provide only the JSON output, no additional text.
        """
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        response = self.bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        try:
            return json.loads(response_body['content'][0]['text'])
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "type": "unknown",
                "color": "unknown",
                "secondary_colors": [],
                "pattern": "unknown",
                "style": "casual",
                "season": ["any"],
                "material": "unknown",
                "gender_category": "unisex",
                "gender_confidence": "low",
                "fit_type": "regular",
                "specific_style": "casual"
            }

    def _enrich_clothing_data(self, clothing_info, user_id):
        """
        Enrich clothing data with user preferences and occasion matching
        """
        # Get user preferences (this would come from your user database)
        user_preferences = self._get_user_preferences(user_id)
        
        # Convert user preferences to sets of strings for comparison
        preferred_colors = set(str(color).lower() for color in user_preferences['preferred_colors'])
        preferred_styles = set(str(style).lower() for style in user_preferences['preferred_styles'])
        
        # Convert clothing info to strings for comparison
        clothing_color = str(clothing_info.get('color', '')).lower()
        clothing_style = str(clothing_info.get('style', '')).lower()
        
        # Add user-specific data
        clothing_info['user_preferences'] = {
            'preferred_color_match': clothing_color in preferred_colors,
            'style_match': clothing_style in preferred_styles,
            'gender_preference_match': clothing_info.get('gender_category') in user_preferences['preferred_gender_categories']
        }
        
        # Add occasion matching
        clothing_info['suitable_occasions'] = self._match_occasions(clothing_info)
        
        return clothing_info

    def _match_occasions(self, clothing_info):
        """
        Match clothing items to suitable occasions based on style and type
        """
        style = str(clothing_info.get('style', '')).lower()
        specific_style = str(clothing_info.get('specific_style', '')).lower()
        
        occasion_mapping = {
            'formal': ['wedding', 'business meeting', 'formal dinner'],
            'business': ['office', 'interview', 'presentation'],
            'casual': ['weekend', 'shopping', 'casual dining'],
            'athletic': ['gym', 'sports', 'outdoor activities'],
            'streetwear': ['casual outings', 'social events', 'urban activities'],
            'bohemian': ['festivals', 'beach', 'casual parties'],
            'classic': ['work', 'dinner', 'social events']
        }
        
        # Combine occasions based on both general and specific style
        occasions = set(occasion_mapping.get(style, []) + occasion_mapping.get(specific_style, []))
        return list(occasions) if occasions else ['casual', 'general']

    def _store_in_s3(self, clothing_data, image_path, user_id):
        """
        Store processed data and image in S3
        """
        # Generate S3 paths
        image_key = f'users/{user_id}/images/{os.path.basename(image_path)}'
        metadata_key = f'users/{user_id}/metadata/{os.path.basename(image_path)}.json'
        
        # Upload image
        with open(image_path, 'rb') as image_file:
            self.s3.upload_fileobj(
                image_file,
                'doojoo-clothes-data',  # Replace with your bucket name
                image_key,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
        
        # Upload metadata
        self.s3.put_object(
            Bucket='doojoo-clothes-data',  # Replace with your bucket name
            Key=metadata_key,
            Body=json.dumps(clothing_data),
            ContentType='application/json'
        )

    def _get_user_preferences(self, user_id):
        """
        Mock function to get user preferences
        Replace with actual database query
        """
        return {
            'preferred_colors': ['blue', 'black', 'white'],
            'preferred_styles': ['casual', 'business casual'],
            'preferred_gender_categories': ['unisex', 'menswear']  # Add gender preferences
        }