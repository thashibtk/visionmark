from .models import Service

def services_context(request):
    """
    Context processor to make services available in all templates
    """
    return {
        'services': Service.objects.all()
    }

