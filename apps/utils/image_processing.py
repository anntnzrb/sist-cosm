"""
Image processing utilities for cosmetics store.
Follows SPARC modularity with functions under 50 lines.
"""
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import io
import logging

logger = logging.getLogger(__name__)


def optimize_image(image_file, max_size=(800, 600), quality=85):
    """
    Optimize uploaded image for web display.
    
    Args:
        image_file: Django UploadedFile instance
        max_size: Tuple of (width, height) maximum dimensions
        quality: JPEG quality (1-100)
    
    Returns:
        Optimized InMemoryUploadedFile
    """
    try:
        # Open and process image
        img = Image.open(image_file)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize while maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Optimize and save
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # Create new uploaded file
        optimized_file = InMemoryUploadedFile(
            output,
            'ImageField',
            f"optimized_{image_file.name}",
            'image/jpeg',
            output.getbuffer().nbytes,
            None
        )
        
        logger.info(f"Image optimized: {image_file.name} -> {optimized_file.size} bytes")
        return optimized_file
        
    except Exception as e:
        logger.error(f"Image optimization failed: {str(e)}")
        return image_file


def create_thumbnail(image_file, size=(150, 150)):
    """
    Create thumbnail from uploaded image.
    
    Args:
        image_file: Django UploadedFile instance
        size: Tuple of (width, height) for thumbnail
    
    Returns:
        Thumbnail as InMemoryUploadedFile
    """
    try:
        img = Image.open(image_file)
        
        # Create square thumbnail with cropping
        thumbnail = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if thumbnail.mode in ('RGBA', 'P'):
            thumbnail = thumbnail.convert('RGB')
        
        # Save thumbnail
        output = io.BytesIO()
        thumbnail.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        # Create thumbnail file
        thumbnail_file = InMemoryUploadedFile(
            output,
            'ImageField',
            f"thumb_{image_file.name}",
            'image/jpeg',
            output.getbuffer().nbytes,
            None
        )
        
        return thumbnail_file
        
    except Exception as e:
        logger.error(f"Thumbnail creation failed: {str(e)}")
        return None


def validate_image_file(image_file, max_size_mb=5):
    """
    Validate uploaded image file.
    
    Args:
        image_file: Django UploadedFile instance
        max_size_mb: Maximum file size in megabytes
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    max_size_bytes = max_size_mb * 1024 * 1024
    if image_file.size > max_size_bytes:
        return False, f"Image size must be less than {max_size_mb}MB"
    
    # Check content type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if image_file.content_type not in allowed_types:
        return False, "Only JPEG, PNG, GIF, and WebP images are allowed"
    
    # Validate image can be opened
    try:
        img = Image.open(image_file)
        img.verify()
        image_file.seek(0)  # Reset file pointer
        return True, ""
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def add_watermark(image_file, watermark_text="Cosméticos Store"):
    """
    Add watermark to image.
    
    Args:
        image_file: Django UploadedFile instance
        watermark_text: Text to use as watermark
    
    Returns:
        Watermarked InMemoryUploadedFile
    """
    try:
        from PIL import ImageDraw, ImageFont
        
        img = Image.open(image_file)
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Calculate position (bottom right)
        text_width = draw.textlength(watermark_text, font=font)
        text_height = 25
        x = img.width - text_width - 10
        y = img.height - text_height - 10
        
        # Add watermark with shadow effect
        draw.text((x+1, y+1), watermark_text, font=font, fill=(0, 0, 0, 128))
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 180))
        
        # Save watermarked image
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        
        watermarked_file = InMemoryUploadedFile(
            output,
            'ImageField',
            f"watermarked_{image_file.name}",
            'image/jpeg',
            output.getbuffer().nbytes,
            None
        )
        
        return watermarked_file
        
    except Exception as e:
        logger.error(f"Watermark addition failed: {str(e)}")
        return image_file