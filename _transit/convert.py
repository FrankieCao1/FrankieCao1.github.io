import os
from PIL import Image, ImageOps

def convert_to_uncut_webp(directory="."):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    processed_count = 0

    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in valid_extensions:
            input_path = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(directory, f"{base_name}.webp")
            
            try:
                with Image.open(input_path) as img:
                    img = ImageOps.exif_transpose(img)
                    img = img.convert("RGBA")
                    
                    # ImageOps.pad shrinks the image so the longest side fits exactly within 512,
                    # and adds padding to the shorter sides so the final file is 512x512.
                    # color=(255, 255, 255, 0) creates a completely transparent border.
                    padded_img = ImageOps.pad(
                        img, 
                        (512, 512), 
                        method=Image.Resampling.LANCZOS,
                        color=(255, 255, 255, 0)
                    )
                    
                    # Save as optimized WebP
                    padded_img.save(output_path, 'webp', optimize=True, quality=85)
                    
                    print(f"✅ Converted & Padded: {filename} -> {base_name}.webp")
                    processed_count += 1
                    
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

    print(f"\nFinished! Successfully processed {processed_count} images.")

if __name__ == "__main__":
    convert_to_uncut_webp()