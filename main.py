#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hotnews import hotnews

scraper = hotnews.NewsScraper(60)
scraper.loop()
