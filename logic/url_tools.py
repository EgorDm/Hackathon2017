import validators

def valid_url(url):
    return not not validators.url(url)
