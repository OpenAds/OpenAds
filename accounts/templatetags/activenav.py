from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active_nav(request, url):
    if request.path == reverse(url):
        return "active"
    return ""