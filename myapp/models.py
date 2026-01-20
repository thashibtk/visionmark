from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from .utils import compress_image

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    details_title = models.CharField(max_length=255)
    details_description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            compressed = compress_image(self.image)
            if compressed:
                self.image = compressed
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = CKEditor5Field('Text', config_name='default')
    excerpt = models.TextField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.featured_image:
            compressed = compress_image(self.featured_image)
            if compressed:
                self.featured_image = compressed
        super().save(*args, **kwargs)


class News(models.Model):
    class NewsType(models.TextChoices):
        ANNOUNCEMENT = 'announcement', 'Announcement'
        EVENT = 'event', 'Event'
        UPDATE = 'update', 'Update'
        CAREER = 'career', 'Career'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    news_type = models.CharField(max_length=20, choices=NewsType.choices, default=NewsType.ANNOUNCEMENT)
    location = models.CharField(max_length=255, blank=True)
    content = CKEditor5Field('Details', config_name='default')
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'News & Update'
        verbose_name_plural = 'News & Updates'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.featured_image:
            compressed = compress_image(self.featured_image)
            if compressed:
                self.featured_image = compressed
        super().save(*args, **kwargs)


class Product(models.Model):
    class Category(models.TextChoices):
        EYEGLASSES = 'eyeglasses', 'Eyeglasses'
        SUNGLASSES = 'sunglasses', 'Sunglasses'
        CONTACT_LENSES = 'contact_lenses', 'Contact Lenses'
        ACCESSORIES = 'accessories', 'Accessories'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.EYEGLASSES)
    brand = models.CharField(max_length=120, blank=True)
    size = models.CharField(max_length=64, blank=True)
    short_description = models.CharField(max_length=400, blank=True)
    description = CKEditor5Field('Description', config_name='default')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.8,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    stock = models.PositiveIntegerField(default=0)
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.main_image:
            compressed = compress_image(self.main_image)
            if compressed:
                self.main_image = compressed
        super().save(*args, **kwargs)

    def get_primary_gallery_image(self):
        return (
            self.gallery.filter(is_primary=True).order_by('sort_order').first()
            or self.gallery.order_by('sort_order').first()
        )

    def get_main_image_url(self):
        if self.main_image:
            return self.main_image.url
        primary_image = self.get_primary_gallery_image()
        return primary_image.image.url if primary_image else ''

    def get_hover_image_url(self):
        primary_image = self.get_primary_gallery_image()
        gallery_qs = self.gallery.order_by('sort_order')
        if primary_image:
            gallery_qs = gallery_qs.exclude(pk=primary_image.pk)
        hover_image = gallery_qs.first()
        if hover_image:
            return hover_image.image.url
        if primary_image:
            return primary_image.image.url
        if self.main_image:
            return self.main_image.url
        return ''


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} image"

    def save(self, *args, **kwargs):
        if self.image:
            compressed = compress_image(self.image)
            if compressed:
                self.image = compressed
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    date = models.DateField(blank=True, null=True)
    is_google_review = models.BooleanField(default=False, help_text="Show Google icon if checked")
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-date', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.rating}/5.0"
    
    def get_rating_stars(self):
        """Returns the number of full stars (integer)"""
        return int(self.rating)