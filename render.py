# -*- coding: utf-8 -*-
import time
import glob
import codecs
import os.path
from dateutil import parser

import markdown

from jinja2 import Environment, FileSystemLoader


class Post:
    def __init__(self, html, date_created, date_modified):
        self.html = html
        self.date_created = date_created
        self.date_modified = date_modified


LAYOUT = Environment(loader=FileSystemLoader('./_layout'))
template = LAYOUT.get_template('base.html')

posts_raw = []
for fpath in glob.iglob('_posts/*.md'):
    post_html = markdown.markdown(
        codecs.open(fpath, mode='r', encoding='utf-8').read(),
        extensions=['fenced_code']
    )
    post_modified = time.ctime(os.path.getmtime(fpath))
    post_created = time.ctime(os.path.getctime(fpath))

    posts_raw.append([parser.parse(post_created), post_html, post_modified])
posts_raw = reversed(sorted(posts_raw, key=lambda x: x[0]))

posts = []
for post in posts_raw:
    posts.append(Post(post[1], post[0], post[2]))

html = template.render(posts=posts)
with open('docs/index.html', 'w', encoding='utf-8') as out_f:
    out_f.write(html)