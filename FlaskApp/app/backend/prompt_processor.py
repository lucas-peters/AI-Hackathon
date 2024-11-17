import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin
import logging
from fake_useragent import UserAgent
import sys

class DoojooRecommendationSystem:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize user agent rotator
        try:
            self.ua = UserAgent()
        except:
            self.ua = None
            self.logger.warning("Couldn't initialize UserAgent, using fallback headers")
        
        self.base_url = "https://www.amazon.com"
        self.session = requests.Session()
        
    def get_headers(self):
        """Generate new headers for each request"""
        if self.ua:
            user_agent = self.ua.random
        else:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]
            user_agent = random.choice(user_agents)
            
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def get_search_url(self, query):
        """Generate search URL with necessary parameters"""
        query = query.replace(' ', '+')
        return f"{self.base_url}/s?k={query}&ref=nb_sb_noss_2"

    def make_request(self, url, retries=3):
        """Make HTTP request with retries and error handling"""
        for attempt in range(retries):
            try:
                headers = self.get_headers()
                self.logger.info(f"Attempting request to {url} (attempt {attempt + 1}/{retries})")
                
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=10
                )
                
                # Log response status
                self.logger.info(f"Response status code: {response.status_code}")
                
                if response.status_code == 200:
                    return response
                
                # Handle specific status codes
                if response.status_code == 503:
                    self.logger.warning("Service unavailable, waiting before retry...")
                    time.sleep(5 * (attempt + 1))
                elif response.status_code == 404:
                    self.logger.error("Page not found")
                    return None
                    
            except requests.RequestException as e:
                self.logger.error(f"Request failed: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2)
                    
        return None

    def extract_products(self, html_content):
        """Extract product information from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        
        # Debug log
        self.logger.info("Starting product extraction")
        
        # Find all product containers
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        self.logger.info(f"Found {len(product_containers)} product containers")
        
        for container in product_containers[:4]:  # Limit to first 4 products
            try:
                # Extract basic product info
                title_element = container.find('span', {'class': 'a-text-normal'})
                price_element = container.find('span', {'class': 'a-price'})
                image_element = container.find('img', {'class': 's-image'})
                link_element = container.find('a', {'class': 'a-link-normal s-no-outline'})
                
                if not all([title_element, image_element, link_element]):
                    continue
                
                product = {
                    'title': title_element.text.strip() if title_element else None,
                    'image_url': image_element['src'] if image_element else None,
                    'product_url': urljoin(self.base_url, link_element['href']) if link_element else None,
                    'price': price_element.find('span', {'class': 'a-offscreen'}).text.strip() if price_element else 'Price not available'
                }
                
                # Only add product if we have all required fields
                if all(product.values()):
                    products.append(product)
                    self.logger.info(f"Successfully extracted product: {product['title'][:30]}...")
                    
            except Exception as e:
                self.logger.error(f"Error extracting product: {str(e)}")
                continue
                
        return products

    def get_recommendations(self, input_data):
        """Get recommendations based on input data"""
        try:
            # Extract relevant information from input
            processed_data = input_data["processed_data"]
            occasion = processed_data["occasion"]
            weather = processed_data["weather"]
            
            # Filter out NA values and create search query dynamically
            query_parts = []

            if occasion and occasion != "NA":
                query_parts.append(occasion)

            if weather and weather != "NA":
                query_parts.append(weather)

            # Generate search query by joining valid parts with "clothes"
            if query_parts:
                search_query = f"{' '.join(query_parts)} clothes"
            else:
                search_query = "clothes"  # Default search query if all data is NA

            self.logger.info(f"Generated search query: {search_query}")
            
            # Get search URL
            url = self.get_search_url(search_query)
            
            # Make request
            response = self.make_request(url)
            if not response:
                self.logger.error("Failed to get response from Amazon")
                return []
                
            # Extract products
            products = self.extract_products(response.content)
            
            # Log results
            self.logger.info(f"Found {len(products)} products")
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error in get_recommendations: {str(e)}")
            return []

# For testing
if __name__ == "__main__":
    # Sample input data
    input_data = {
        "user_id": "test_user_123",
        "prompt": "Going to a the casino",
        "processed_data": {
            "time": "afternoon",
            "date": "tomorrow",
            "location": "Miami",
            "occasion": "beach party",
            "weather": "warm and sunny",
            "additional_data": "Beach party attire is appropriate, such as swimwear, cover-ups, sandals, sunglasses, and sun protection."
        }
    }
    
    # Initialize recommender
    recommender = DoojooRecommendationSystem()
    
    # Get recommendations
    recommendations = recommender.get_recommendations(input_data)
    
    # Print results
    if recommendations:
        print(json.dumps(recommendations, indent=2))
    else:
        print("No recommendations found. Check the logs for details.")
