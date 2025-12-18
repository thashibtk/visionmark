from django.shortcuts import render, get_object_or_404
from .models import Service, Blog, News, Product, Testimonial
from django.core.paginator import Paginator

def home(request):
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-date', '-created_at')[:10]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
    services = Service.objects.all()
    return render(request, 'home.html', {
        'testimonials': testimonials,
        'latest_products': latest_products,
        'services': services
    })


def about(request):
    return render(request, 'about.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def servicedetails(request, service_id):
    service = Service.objects.get(id=service_id)
    services = Service.objects.all()

    key_benefits = [
        {"title": "Expert Guidance", "description": "Get support from trained optical professionals."},
        {"title": "Modern Tools", "description": "Accurate results using updated diagnostic equipment."},
        {"title": "Quick Service", "description": "Fast and comfortable experience for every customer."},
        {"title": "Personalized Advice", "description": "Solutions tailored to your needs and lifestyle."},
        {"title": "Affordable Options", "description": "Budget-friendly and premium solutions available."},
        {"title": "Trusted Care", "description": "Safe, reliable, and customer-first optical care."},
    ]

    return render(request, 'servicedetails.html', {
        'service': service,
        'services': services,
        'key_benefits': key_benefits
    })


def faq(request):
    return render(request, 'faqs.html')

def blog_list(request):
    posts = Blog.objects.filter(is_published=True).order_by('-published_at')

    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {
        'page_obj': page_obj
    })

def blog_single(request, slug):
    post = get_object_or_404(Blog, slug=slug, is_published=True)

    # Popular posts = latest 6 excluding current
    popular_posts = Blog.objects.filter(is_published=True).exclude(id=post.id)[:6]

    return render(request, "blog-single.html", {
        "post": post,
        "popular_posts": popular_posts
    })


def news_list(request):
    news_items = News.objects.filter(is_published=True).order_by('-published_at', '-created_at')
    paginator = Paginator(news_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news_list.html', {
        'page_obj': page_obj,
    })


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    recent_news = News.objects.filter(is_published=True).exclude(id=news.id).order_by('-published_at')[:4]

    return render(request, 'news_detail.html', {
        'news': news,
        'recent_news': recent_news
    })

def contact(request):
    return render(request, 'contact.html')

def book_your_visit(request):
    return render(request, 'book-your-visit.html')

def products(request):
    products_qs = (
        Product.objects.filter(is_active=True)
        .order_by('-created_at')
        .prefetch_related('gallery')
    )
    paginator = Paginator(products_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category_choices = Product.Category.choices
    brands = (Product.objects.filter(is_active=True)
              .exclude(brand='')
              .values_list('brand', flat=True)
              .distinct()
              .order_by('brand'))

    return render(request, 'products.html', {
        'page_obj': page_obj,
        'category_choices': category_choices,
        'brands': brands
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related('gallery'), slug=slug, is_active=True)
    gallery = product.gallery.all()
    related_products = Product.objects.filter(is_active=True).exclude(id=product.id).order_by('-created_at')[:4]

    return render(request, 'shop-product-single.html', {
        'product': product,
        'gallery': gallery,
        'related_products': related_products
    })


def testimonials(request):
    testimonials_list = Testimonial.objects.filter(is_published=True).order_by('sort_order', '-date', '-created_at')
    return render(request, 'testimonials.html', {
        'testimonials': testimonials_list
    })


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)