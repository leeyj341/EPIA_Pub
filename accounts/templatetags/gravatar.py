import hashlib
from django import template

register = template.Library()

@register.filter
def makehash(user):
    email = user.email
    return  'https://www.gravatar.com/avatar/' + hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()