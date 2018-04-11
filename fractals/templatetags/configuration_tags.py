from django import template
from django.templatetags.static import static

from fractals.models import Configuration

register = template.Library()


@register.filter
def fractal_url(configuration: Configuration):
    try:
        return configuration.image.url
    except ValueError:
        return static("fractals/default.png")
