from django import template

register = template.Library()

@register.filter()
def message_filter(value):
    if value == 'info':
        return 'primary'
    elif value == 'error':
        return 'danger'
    return value

@register.filter()
def check_negative(value):
    if value < 0:
        return 'Give him {} rupees back'.format(abs(value))
    else:
        return 'Total debit to pay: {}'.format(value)