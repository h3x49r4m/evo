#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "h3x49r4m"
SITENAME = "Evo"
SITEURL = ""

PATH = "_content"

TIMEZONE = "UTC"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (("Pelican", "https://getpelican.com/"),
         ("Python.org", "https://python.org/"),
         ("Jinja2", "https://palletsprojects.com/p/jinja/"),
         ("You can modify those links in your config file", "#"),)

# Social widget
SOCIAL = (("You can add links in your config file", "#"),
          ("Another social link", "#"),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Theme
THEME = "peta-rust"

# Ablog settings
ABLOG = {
    "title": "Evo",
    "blog_title": "Blog",
    "blog_path": "/blog",
    "blog_authors": {
        AUTHOR: ("h3x49r4m", "https://github.com/h3x49r4m"),
    },
    "blog_default_author": AUTHOR,
    "language": "en",
    "postcard_excerpts": True,
    "postcard_image": "images/ablog.png",
    "postcard_image_width": "300px",
}

# Static files
STATIC_PATHS = ["_static"]

# Markdown extensions
MD_EXTENSIONS = ["codehilite", "extra", "toc"]

# Output path
OUTPUT_PATH = "output"