from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field widget."""
    return field.as_widget(attrs={'class': css_class})


@register.filter
def status_badge_class(status):
    """Return CSS class for file status badge."""
    mapping = {
        'normal': 'badge-normal',
        'petition': 'badge-petition',
        'petition_in_progress': 'badge-progress',
        'petition_solved': 'badge-solved',
        'custom': 'badge-custom',
    }
    return mapping.get(status, 'badge-normal')
