import os
from PIL import Image
from pillow_heif import register_heif_opener

def convert_heic_to_bmp():
    # Register HEIF opener with Pillow
    register_heif_opener()
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create bmp output directory if it doesn't exist
    output_dir = os.path.join(script_dir, 'bmp')
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all HEIC files in the directory
    heic_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.heic')]
    
    if not heic_files:
        print("No HEIC files found in the current directory.")
        return
    
    print(f"Found {len(heic_files)} HEIC files to convert.")
    
    # Process each HEIC file
    for heic_file in heic_files:
        try:
            # Open the HEIC file
            input_path = os.path.join(script_dir, heic_file)
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
            output_filename = os.path.splitext(heic_file)[0] + '.bmp'
            output_path = os.path.join(output_dir, output_filename)
            
            # Save as BMP
            image.save(output_path, 'BMP')
            print(f"Converted {heic_file} to {output_filename}")
            
        except Exception as e:
            print(f"Error converting {heic_file}: {str(e)}")

if __name__ == "__main__":
    convert_heic_to_bmp() 