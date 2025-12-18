from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap, ServiceSitemap, ProductSitemap, BlogSitemap, NewsSitemap
from . import views

sitemaps = {
    'static': StaticSitemap,
    'services': ServiceSitemap,
    'products': ProductSitemap,
    'blog': BlogSitemap,
    'news': NewsSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('services/<int:service_id>', views.servicedetails, name='servicedetails'),
    path('faq', views.faq, name='faq'),
    path('blog', views.blog_list, name='blog_list'),
    path("blog/<slug:slug>/", views.blog_single, name="blog_single"),
    path('news', views.news_list, name='news_list'),
    path('news/<slug:slug>', views.news_detail, name='news_detail'),
    path('contact', views.contact, name='contact'),
    path('book-your-visit', views.book_your_visit, name='book_your_visit'),
    path('products', views.products, name='products'),
    path('products/<slug:slug>', views.product_detail, name='product_detail'),
    path('testimonials', views.testimonials, name='testimonials'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]