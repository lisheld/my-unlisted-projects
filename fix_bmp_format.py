import os
from PIL import Image

def fix_bmp_format_for_circuitpython():
    """Fix BMP format to ensure CircuitPython recognizes them as indexed color"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bmp_dir = os.path.join(script_dir, 'bmp')
    
    if not os.path.exists(bmp_dir):
        print("No bmp directory found!")
        return
    
    bmp_files = [f for f in os.listdir(bmp_dir) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        print("No BMP files found.")
        return
    
    print(f"Found {len(bmp_files)} BMP files to fix for CircuitPython compatibility.")
    
    for bmp_file in bmp_files:
        try:
            input_path = os.path.join(bmp_dir, bmp_file)
            
            print(f"Processing {bmp_file}...")
            image = Image.open(input_path)
            
            print(f"  Original mode: {image.mode}")
            
            # Ensure we're working with RGB first
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create indexed image with specific settings for CircuitPython
            print("  Converting to indexed color with optimized settings...")
            indexed_image = image.quantize(
                colors=32, 
                method=Image.Quantize.MEDIANCUT,
                dither=Image.Dither.NONE  # No dithering for cleaner palette
            )
            
            # Ensure we have a proper palette
            if indexed_image.mode != 'P':
                print(f"  Warning: Image mode is {indexed_image.mode}, not P")
                continue
                
            print(f"  Final mode: {indexed_image.mode}")
            print(f"  Palette colors: {len(indexed_image.getpalette())//3}")
            
            # Save with specific BMP format options
            indexed_image.save(
                input_path, 
                'BMP',
                bitmap_format='bmp',  # Ensure BMP format
                bits=8  # 8-bit indexed color
            )
            
            # Verify the saved file
            test_image = Image.open(input_path)
            print(f"  Verified saved mode: {test_image.mode}")
            
            file_size = os.path.getsize(input_path)
            print(f"  File size: {file_size} bytes")
            print(f"  ✓ Fixed {bmp_file}")
            
        except Exception as e:
            print(f"  ✗ Error fixing {bmp_file}: {str(e)}")
    
    print("\nBMP format fix complete!")

if __name__ == "__main__":
    fix_bmp_format_for_circuitpython() 