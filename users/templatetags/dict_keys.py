from django.template.defaultfilters import register

@register.filter(name='dict_key')
def dict_key(d, k):
    return d[k]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)