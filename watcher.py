#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import time
from urlparse import urlparse

import feedparser
from pelican import main as static_generator
from pelican.readers import MarkdownReader
from pelican.contents import Article
from pelican.utils import SafeDatetime

from pelicanconf import (PROJECT_DIR, PATH, FEED_URL, UPDATE_TIME,
                         DISQUS_API_KEY, DEFAULT_PAGINATION)


class Watcher(object):

    def __init__(self):
        self.limit = DEFAULT_PAGINATION
        self.articles = []
        self._read_articles()
        self.last_imported_article = self._get_last_imported()

    def _read_articles(self):
        content_path = os.path.join(PROJECT_DIR, PATH)
        reader = MarkdownReader({
            'MD_EXTENSIONS': ['codehilite(css_class=highlight)', 'extra']
        })
        for file in os.listdir(content_path):
            if file.endswith('.md'):
                content, metadata = reader.read(
                    os.path.join(content_path, file)
                )
                self.articles.append({
                        'content': content,
                        'metadata': metadata
                    })

    def _get_last_imported(self):
        last_imported_aticle = None
        for article in self.articles:
            if not last_imported_aticle:
                last_imported_aticle = article
            elif article['metadata']['date'] > last_imported_aticle['metadata']['date']:
                last_imported_aticle = article
        return last_imported_aticle

    def _write_markdown(self, title, date, link, content):
        md_template = u"""Title: %(title)s.
Date: %(date)s
Link: %(link)s
Domain: %(domain)s
Category: all

%(content)s"""
        metadata = {
            'date': date,
            'link': link,
            'title': title
        }
        filename = u'%s.md' % Article(content, metadata=metadata).url
        self.articles.append({
            'content': content,
            'metadata': metadata
        })
        self.last_imported_article = self._get_last_imported()
        parsed_link = urlparse(link.encode('utf-8').decode('utf-8'))
        data = md_template % {
            'title': title.encode('utf-8').decode('utf-8'),
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'link': link.encode('utf-8').decode('utf-8'),
            'content': content.encode('utf-8').decode('utf-8'),
            'domain': u'%s://%s' % (parsed_link.scheme, parsed_link.netloc)
        }
        _file = open(os.path.join(PROJECT_DIR, PATH, filename), 'w+')
        _file.write(data.encode('utf-8'))
        _file.close()
        print 'Saved: %s'% filename
        return True

    def _check_close_previous_threads(self):
        # TODO: https://disqus.com/api/docs/threads/close/
        # self._save_state()
        pass

    def _import_entry(self, entry):
        self._write_markdown(
            entry.title,
            entry.published_parsed,
            entry.link,
            entry.description)
        self._check_close_previous_threads()
        static_generator()
        
    def fetch(self):
        feed = feedparser.parse(FEED_URL)
        i = 0
        for entry in feed.entries:
            entry.published_parsed = SafeDatetime(*entry.published_parsed[:6])
            if i == self.limit:
                return False
            if self.last_imported_article and \
               entry.published_parsed <= self.last_imported_article['metadata']['date']:
                i += 1
                continue
            self._import_entry(entry)
            i += 1
        return True

    def run(self):
        while True:
            self.fetch()
            time.sleep(UPDATE_TIME)


if __name__ == '__main__':
    watcher = Watcher()
    watcher.run()
