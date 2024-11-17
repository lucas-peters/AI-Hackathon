import os
import kaggle
import shutil
from tqdm import tqdm

def download_and_prepare_dataset():
    # Create directories if they don't exist
    if not os.path.exists('raw_dataset'):
        os.makedirs('raw_dataset')
    if not os.path.exists('test_images'):
        os.makedirs('test_images')

    # Download the dataset
    print("Downloading dataset...")
    kaggle.api.dataset_download_files(
        'paramaggarwal/fashion-product-images-small', 
        path='raw_dataset', 
        unzip=True
    )

    # Select and copy a subset of images
    print("\nPreparing test images...")
    source_dir = 'raw_dataset/images'
    target_dir = 'test_images'
    
    # Get list of image files
    image_files = [f for f in os.listdir(source_dir) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Select first 10 images
    selected_images = image_files[:10]
    
    # Copy selected images to test_images directory
    for image in tqdm(selected_images, desc="Copying images"):
        source_path = os.path.join(source_dir, image)
        target_path = os.path.join(target_dir, image)
        shutil.copy2(source_path, target_path)
    
    print(f"\nSuccessfully prepared {len(selected_images)} images in {target_dir}/")
    print("You can now run your image processing pipeline!")

if __name__ == "__main__":
    try:
        download_and_prepare_dataset()
    except Exception as e:
        print(f"Error: {str(e)}")