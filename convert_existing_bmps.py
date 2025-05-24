import os
from PIL import Image

def convert_existing_bmps_to_indexed():
    """Convert existing BMP files to indexed color format"""
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # BMP directory
    bmp_dir = os.path.join(script_dir, 'bmp')
    backup_dir = os.path.join(script_dir, 'bmp_backup')
    
    if not os.path.exists(bmp_dir):
        print("No bmp directory found!")
        return
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Find all BMP files
    bmp_files = [f for f in os.listdir(bmp_dir) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        print("No BMP files found in bmp directory.")
        return
    
    print(f"Found {len(bmp_files)} BMP files to convert to indexed color.")
    
    # Process each BMP file
    for bmp_file in bmp_files:
        try:
            input_path = os.path.join(bmp_dir, bmp_file)
            backup_path = os.path.join(backup_dir, bmp_file)
            
            # Create backup
            print(f"Backing up {bmp_file}...")
            with open(input_path, 'rb') as src, open(backup_path, 'wb') as dst:
                dst.write(src.read())
            
            # Open the BMP file
            print(f"Converting {bmp_file} to indexed color...")
            image = Image.open(input_path)
            
            # Check current mode
            print(f"  Current mode: {image.mode}")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to indexed color with 32 colors
            indexed_image = image.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
            
            print(f"  New mode: {indexed_image.mode}")
            print(f"  Palette colors: {len(indexed_image.getpalette())//3}")
            
            # Save back as indexed color BMP
            indexed_image.save(input_path, 'BMP')
            
            # Check file size difference
            original_size = os.path.getsize(backup_path)
            new_size = os.path.getsize(input_path)
            print(f"  Size: {original_size} -> {new_size} bytes")
            print(f"  ✓ Converted {bmp_file} successfully!")
            
        except Exception as e:
            print(f"  ✗ Error converting {bmp_file}: {str(e)}")
    
    print(f"\nConversion complete! Original files backed up to bmp_backup/")
    print("You can now upload the converted BMP files to GitHub.")

if __name__ == "__main__":
    convert_existing_bmps_to_indexed() 