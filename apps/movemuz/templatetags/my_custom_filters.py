from django import template
from django.db.models.fields.related import ForeignKey

register = template.Library()

@register.filter
def get_verbose_name(obj, field_name):
    """Returns the verbose name of a field for a given model instance."""
    try:
        return obj._meta.get_field(field_name).verbose_name
    except:
        return field_name

@register.filter
def get_field_value(obj, field_name):
    """Returns the value of a field for a given model instance."""
    return getattr(obj, field_name)

@register.filter
def get_related_field_value(obj, field_name):
    """Returns the __str__ representation of a related object."""
    try:
        related_obj = getattr(obj, field_name)
        if related_obj:
            return str(related_obj)
        return ""
    except AttributeError:
        return ""

@register.filter
def get_item(dictionary, key):
    """Allows accessing dictionary items in Django templates."""
    return dictionary.get(key)

@register.filter
def get_condicao_manutencao_display(obj):
    """Returns the human-readable display for condicao_manutencao field."""
    return obj.get_condicao_manutencao_display()