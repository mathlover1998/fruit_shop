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

register.filter('is_recent', is_recent)