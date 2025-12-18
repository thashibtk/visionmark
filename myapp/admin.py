from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Service, Blog, News, Product, ProductImage, Testimonial
from .forms import ProductAdminForm

# Register your models here.

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'image_preview', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    @display(description="Image Preview", ordering=True)
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'featured_image_preview', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['featured_image_preview', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    @display(description="Featured Image", ordering=True)
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return "No image"


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ['title', 'featured_image_preview', 'news_type', 'location', 'is_published', 'published_at']
    list_filter = ['news_type', 'is_published', 'published_at']
    search_fields = ['title', 'subtitle', 'content', 'location']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['featured_image_preview', 'created_at', 'updated_at']
    date_hierarchy = 'published_at'
    
    @display(description="Featured Image", ordering=True)
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return "No image"


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_preview', 'alt_text', 'is_primary', 'sort_order']
    readonly_fields = ['image_preview']
    
    @display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 80px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'main_image_preview', 'category', 'brand', 'price', 'sale_price', 'stock', 'is_active']
    list_filter = ['category', 'brand', 'is_active', 'created_at']
    search_fields = ['name', 'sku', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['main_image_preview', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    @display(description="Main Image", ordering=True)
    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                obj.main_image.url
            )
        # Try to get from gallery
        primary_image = obj.get_primary_gallery_image()
        if primary_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                primary_image.image.url
            )
        return "No image"


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['name', 'rating', 'is_google_review', 'is_published', 'date', 'sort_order']
    list_filter = ['is_published', 'is_google_review', 'date', 'created_at']
    search_fields = ['name', 'comment']
    list_editable = ['is_published', 'sort_order']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Testimonial Information', {
            'fields': ('name', 'comment', 'rating', 'date')
        }),
        ('Display Settings', {
            'fields': ('is_google_review', 'is_published', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
