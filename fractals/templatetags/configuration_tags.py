from django import template
from django.templatetags.static import static

from fractals.models import Configuration

register = template.Library()


@register.filter
def fractal_url(configuration: Configuration):
    if configuration.image is not None:
        return configuration.image.url
    return static("fractals/default.png")
