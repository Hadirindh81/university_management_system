# core/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Return d.get(key) safely from templates."""
    try:
        if d is None:
            return None
        return d.get(key)
    except Exception:
        return None

# also register alias 'get_item' in case older templates use it
register.filter('get_item', dict_get)
