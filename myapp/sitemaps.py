from django.contrib import sitemaps
from django.urls import reverse
from .models import Service, Blog, News, Product

class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 'about', 'services', 'faq', 'contact', 
            'book_your_visit', 'products', 'testimonials'
        ]

    def location(self, item):
        return reverse(item)

class ServiceSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('servicedetails', args=[obj.id])

class ProductSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)
    
    def location(self, obj):
        return reverse('product_detail', args=[obj.slug])

class BlogSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('blog_single', args=[obj.slug])

class NewsSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return News.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('news_detail', args=[obj.slug])
