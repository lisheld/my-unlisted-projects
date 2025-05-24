import os
from PIL import Image

def convert_to_pcx_format():
    """Convert BMP files to PCX format for better CircuitPython palette support"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bmp_dir = os.path.join(script_dir, 'bmp')
    
    if not os.path.exists(bmp_dir):
        print("No bmp directory found!")
        return
    
    bmp_files = [f for f in os.listdir(bmp_dir) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        print("No BMP files found.")
        return
    
    print(f"Found {len(bmp_files)} BMP files to convert to PCX format.")
    
    for bmp_file in bmp_files:
        try:
            input_path = os.path.join(bmp_dir, bmp_file)
            
            # Create PCX filename
            pcx_filename = os.path.splitext(bmp_file)[0] + '.pcx'
            output_path = os.path.join(bmp_dir, pcx_filename)
            
            print(f"Converting {bmp_file} to {pcx_filename}...")
            image = Image.open(input_path)
            
            print(f"  Original mode: {image.mode}")
            
            # Ensure RGB first
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create indexed image
            indexed_image = image.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
            
            print(f"  Indexed mode: {indexed_image.mode}")
            print(f"  Colors: {len(indexed_image.getpalette())//3}")
            
            # Save as PCX
            indexed_image.save(output_path, 'PCX')
            
            file_size = os.path.getsize(output_path)
            print(f"  PCX size: {file_size} bytes")
            print(f"  ✓ Created {pcx_filename}")
            
        except Exception as e:
            print(f"  ✗ Error converting {bmp_file}: {str(e)}")
    
    print("\nPCX conversion complete!")
    print("Update your IMAGE_URLS to use .pcx files instead of .bmp files")

if __name__ == "__main__":
    convert_to_pcx_format() 