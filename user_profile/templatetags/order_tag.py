from django import template

register = template.Library('user_profile')

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)