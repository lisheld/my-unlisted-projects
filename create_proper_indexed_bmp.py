import os
from PIL import Image

def create_proper_indexed_bmps():
    """Create BMP files in 8-bit indexed format that CircuitPython should recognize"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bmp_dir = os.path.join(script_dir, 'bmp')
    
    if not os.path.exists(bmp_dir):
        print("No bmp directory found!")
        return
    
    bmp_files = [f for f in os.listdir(bmp_dir) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        print("No BMP files found.")
        return
    
    print(f"Found {len(bmp_files)} BMP files to convert to proper indexed format.")
    
    for bmp_file in bmp_files:
        try:
            input_path = os.path.join(bmp_dir, bmp_file)
            
            print(f"Processing {bmp_file}...")
            image = Image.open(input_path)
            
            print(f"  Original mode: {image.mode}")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Try with fewer colors first - sometimes works better
            print("  Creating 16-color indexed image...")
            indexed_image = image.quantize(
                colors=16,  # Reduced from 32 to 16 colors
                method=Image.Quantize.MEDIANCUT,
                dither=Image.Dither.NONE
            )
            
            print(f"  Mode after quantize: {indexed_image.mode}")
            print(f"  Palette colors: {len(indexed_image.getpalette())//3}")
            
            # Save with very specific BMP options for compatibility
            print("  Saving as 8-bit indexed BMP...")
            indexed_image.save(
                input_path,
                'BMP',
                optimize=False,  # Don't optimize - keep it simple
                compression='raw'  # No compression for maximum compatibility
            )
            
            # Verify what we saved
            test_load = Image.open(input_path)
            print(f"  Verified saved mode: {test_load.mode}")
            
            file_size = os.path.getsize(input_path)
            print(f"  File size: {file_size} bytes")
            print(f"  ✓ Converted {bmp_file}")
            
        except Exception as e:
            print(f"  ✗ Error processing {bmp_file}: {str(e)}")
    
    print("\nIndexed BMP creation complete!")

if __name__ == "__main__":
    create_proper_indexed_bmps() 