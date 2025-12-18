from django import template

register = template.Library()


@register.filter
def star_rating(value):
    """
    Returns a list of Font Awesome star icon classes
    For 4.3: shows 4 full stars + 1 half star + 0 empty stars
    """
    try:
        rating = float(value or 0)
    except (ValueError, TypeError):
        rating = 0.0
    
    # Clamp rating between 0 and 5
    rating = max(0.0, min(5.0, rating))
    
    stars = []
    full_stars = int(rating)
    decimal_part = rating - full_stars
    
    # Add full stars (fas fa-star)
    for _ in range(full_stars):
        stars.append('fas fa-star')
    
    # Add half star if there's a decimal part (any value > 0 and < 1)
    # This handles cases like 4.3, 4.1, 4.7, etc.
    if decimal_part > 0 and full_stars < 5:
        stars.append('fas fa-star-half-stroke')
    
    # Add empty stars (far fa-star) to make exactly 5 total
    while len(stars) < 5:
        stars.append('far fa-star')
    
    return stars[:5]