from django import template

register = template.Library()


@register.filter
def total_amount(entry_count, amount_to_enter):
    return int(entry_count) * int(amount_to_enter)

