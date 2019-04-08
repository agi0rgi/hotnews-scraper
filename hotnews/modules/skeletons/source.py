#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Source():
	"""
	Guideline to the others news scraper modules
	"""
	def __init__(self,homepage,lastNews,articles,websitename = ""):
		self.homepage = homepage
		self.websitename = websitename
		self._lastNews = lastNews
		self._articles = articles

	def getLastNews(self):
		raise NotImplementedError

	def _findAvailableArticles_(self):
		return

	def getAvailableArticles(self):
		"""

		Params: None
		Returns: List
	
		This method returns the list of the articles

		"""
		self._findAvailableArticles_()
		return self._articles

	def getArticle(self,index):
		"""

		Params: Index (int)
		Returns: News (Object)
	
		This method returns the article at <index> position

		"""
		self._findAvailableArticles_()
		return self._articles[index]
