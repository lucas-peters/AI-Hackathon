from clothing_processor import ClothingImageProcessor
import os

def test_single_upload():
    # Initialize the processor
    processor = ClothingImageProcessor()
    
    # Test directory with some sample images
    test_dir = "test_images"
    
    # Create test directory if it doesn't exist
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created directory: {test_dir}")
        print("Please add some clothing images to this directory before running the test")
        return
    
    # Process each image in the test directory
    for image_file in os.listdir(test_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"\nProcessing image: {image_file}")
            try:
                image_path = os.path.join(test_dir, image_file)
                result = processor.process_image(image_path, "test_user_123")
                print("Successfully processed image!")
                print("Extracted information:")
                print(f"Type: {result['type']}")
                print(f"Color: {result['color']}")
                print(f"Style: {result['style']}")
                print(f"Season: {result['season']}")
                print("Suitable occasions:", ', '.join(result['suitable_occasions']))
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

if __name__ == "__main__":
    test_single_upload()