from datetime import timedelta
from django import template
from django.utils import timezone

register = template.Library()


def is_recent(target_datetime):
    now = timezone.now()
    
    # Calculate the difference between the current datetime and the target datetime
    difference = now - target_datetime
    
    # Check if the difference is less than 1 week (7 days)
    if difference < timedelta(days=7):
        return True
    else:
        return False


def replace_filter(value, new):
    new_words = value.replace('_count', new)
    words = new_words.split('_')
    return ' '.join(word.capitalize() for word in words)


def snake_case_filter(s):
    result = ''
    for i, char in enumerate(s):
        if i > 0 and char.isupper():
            result += '_'
        result += char.lower()
    return result

def snake_case_to_title_case(string):
    return string.replace('_', ' ').title()

def mul(value,number):
    return value*number


register.filter('is_recent', is_recent)
register.filter('replace',replace_filter)
register.filter('snake_case_filter',snake_case_filter)
register.filter('snake_case_to_title_case',snake_case_to_title_case)
register.filter('mul',mul)