"""
Script to create PWA icons from a base image.
Place a 512x512 PNG image named 'icon-base.png' in the static/icons/ directory
and run this script to generate all required icon sizes.
"""
from PIL import Image
import os

def create_icons():
    base_path = os.path.join('static', 'icons', 'icon-base.png')
    output_dir = os.path.join('static', 'icons')
    
    if not os.path.exists(base_path):
        print("❌ icon-base.png not found!")
        print("Please create a 512x512 PNG image and save it as static/icons/icon-base.png")
        return
    
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    try:
        base_image = Image.open(base_path)
        
        for size in sizes:
            # Resize image maintaining aspect ratio
            resized = base_image.resize((size, size), Image.Resampling.LANCZOS)
            output_path = os.path.join(output_dir, f'icon-{size}.png')
            resized.save(output_path, 'PNG', optimize=True)
            print(f"✅ Created icon-{size}.png")
        
        print("\n🎉 All icons created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
        print("\nNote: Install Pillow with: pip install Pillow")

if __name__ == '__main__':
    create_icons()





