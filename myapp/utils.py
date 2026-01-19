import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(image_field, quality=80):
    """
    Compresses the image and converts it to WebP format.
    """
    if not image_field:
        return

    # Check if the image has already been converted to WebP
    if image_field.name.lower().endswith('.webp'):
        return

    try:
        # Open the image using Pillow
        img = Image.open(image_field)
        
        # Convert to RGB if necessary (e.g. for PNGs with transparency, 
        # though WebP handles transparency, sometimes it's safer to convert if saving as non-alpha)
        # WebP supports RGBA, so we can keep it if needed, but 'RGB' is safer for general compression
        # if the user doesn't strictly need transparency everywhere. 
        # However, for product images, transparent backgrounds might be desirable.
        # Let's simple check modes.
        if img.mode in ('RGBA', 'LA') and 'jpg' in image_field.name.lower():
             # If source looked like jpg but had alpha, weird, but okay.
             # Generally we might want to preserve alpha for WebP.
             pass
        
        # Determine the new filename
        file_name = image_field.name.split('.')[0] + '.webp'
        
        # Create a BytesIO object to hold the new image data
        output = BytesIO()
        
        # Save the image to the BytesIO object in WebP format
        img.save(output, format='WEBP', quality=quality, optimize=True)
        output.seek(0)
        
        # Create a new InMemoryUploadedFile
        new_image = InMemoryUploadedFile(
            output,
            'ImageField',
            file_name,
            'image/webp',
            sys.getsizeof(output),
            None
        )
        
        # Assign the new image to the field
        return new_image

    except Exception as e:
        print(f"Error compressing image: {e}")
        return None
