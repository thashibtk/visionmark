from django.urls import path
from . import views

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
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
]