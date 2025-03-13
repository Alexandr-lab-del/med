from django import template

register = template.Library()


@register.filter
def chunks(value, chunk_size):
    try:
        chunk_size = int(chunk_size)
    except (ValueError, TypeError):
        return [value]

    if not value:
        return []

    return [value[i:i + chunk_size] for i in range(0, len(value), chunk_size)]
