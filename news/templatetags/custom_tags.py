from django import template
from news.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag(name="check_auth_page")
def check_page(request):
    return request.path in ("/auth/login/", "/auth/registration/")
