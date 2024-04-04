from datetime import timedelta, date
from django import template

register = template.Library()

@register.filter
def is_recent(date_str):
    current_date = date.today()
    
    # Calculate the difference between the current date and the checked date
    difference = current_date - date_str
    
    # Check if the difference is less than 1 week (7 days)
    if difference < timedelta(days=7):
        return True
    else:
        return False

@register.filter
def replace_filter(value, new):
    new_words = value.replace('_count', new)
    words = new_words.split('_')
    return ' '.join(word.capitalize() for word in words)

@register.filter
def snake_case_filter(s):
    result = ''
    for i, char in enumerate(s):
        if i > 0 and char.isupper():
            result += '_'
        result += char.lower()
    return result

register.filter('is_recent', is_recent)
register.filter('replace',replace_filter)
register.filter('snake_case_filter',snake_case_filter)