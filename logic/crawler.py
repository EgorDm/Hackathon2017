import re
import ssl
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, Comment

import logic.constants as constants

allowed_types = ['h1', 'h2', 'h3', 'h5', 'h6', 'p', 'h1']


def scrap_page(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    q = Request(url)
    html = urlopen(q).read()
    ret = _first_pass(html)
    ret = _second_pass(ret)
    ret = _third_pass(ret)
    return ret


def _first_pass(document):
    soup = BeautifulSoup(document, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    for comments in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comments.extract()
    for tag in constants.tag_blacklist:
        [x.extract() for x in soup.findAll(tag)]
    for cls in constants.class_blacklist:
        for possible_link in soup.find_all(constants.filterable_tags, {'class': re.compile(r'(?i).*' + cls + '.*')}):
            possible_link.extract()
        for possible_link in soup.find_all(constants.filterable_tags, {'id': re.compile(r'(?i).*' + cls + '.*')}):
            possible_link.extract()
    for match in soup.findAll(constants.unwrap_tags):
        match.unwrap()
    return soup


def _second_pass(soup):
    for match in soup.findAll('a'):
        if match.parent == None: continue
        if match.parent.name == 'li':
            match.parent.extract()
    for match in soup.findAll('a'):
        match.unwrap()
    return soup


def _third_pass(soup):
    extr = extract_text(soup)
    normalized = []
    for line in extr:
        if len(normalized) > 0 and normalized[-1][1] == line[1]:
            normalized[-1][0] += line[0]
        else:
            normalized.append(line)
    return normalized


def extract_text(root, min_len=3):
    ret = []
    if root.string is not None and len(root.string.split()) >= min_len:
        tag = root.name if root.name is not None else root.parent.name
        ret.append([root.string, tag if tag in allowed_types else 'p'])
    if hasattr(root, 'children'):
        for child in root.children:
            ret += extract_text(child, min_len)
    return ret

def special_to_html(extr):
    doc = ''
    for line in extr:
        doc += '<{0}>{1}</{0}>'.format(line[1], line[0])
    doc = doc.replace('\n', '<br>')
    return doc

def special_to_text(extr):
    lines = [line[0] for line in extr]
    return ' '.join(lines)