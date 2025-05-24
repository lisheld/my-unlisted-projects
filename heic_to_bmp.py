import os
from PIL import Image
from pillow_heif import register_heif_opener

def convert_images_to_bmp():
    # Register HEIF opener with Pillow
    register_heif_opener()
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create bmp output directory if it doesn't exist
    output_dir = os.path.join(script_dir, 'bmp')
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all supported image files in the directory
    image_files = [f for f in os.listdir(script_dir) if f.lower().endswith(('.heic', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No supported image files (HEIC, JPG, JPEG) found in the current directory.")
        return
    
    print(f"Found {len(image_files)} image files to convert.")
    
    # Process each image file
    for image_file in image_files:
        try:
            # Open the image file
            input_path = os.path.join(script_dir, image_file)
            image = Image.open(input_path)
            
            # Convert to RGB mode (24-bit)
            image = image.convert('RGB')
            
            # Get current dimensions
            width, height = image.size
            
            # Calculate square crop dimensions
            if width > height:
                # Landscape image - crop width
                left = (width - height) // 2
                top = 0
                right = left + height
                bottom = height
            else:
                # Portrait image - crop height
                left = 0
                top = (height - width) // 2
                right = width
                bottom = top + width
            
            # Crop to square
            image = image.crop((left, top, right, bottom))
            
            # Resize to 64x64
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
            
            # Create output filename
            output_filename = os.path.splitext(image_file)[0] + '.bmp'
            output_path = os.path.join(output_dir, output_filename)
            
            # Save as BMP
            image.save(output_path, 'BMP')
            print(f"Converted {image_file} to {output_filename}")
            
        except Exception as e:
            print(f"Error converting {image_file}: {str(e)}")

if __name__ == "__main__":
    convert_images_to_bmp() 