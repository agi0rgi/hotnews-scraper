#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .skeletons.news import News
from .skeletons.source import Source
import requests
from bs4 import BeautifulSoup

class Corriere(Source):
	def __init__(self):
		homepage = "http://www.corriere.it"
		name = "Corriere"
		Source.__init__(self,homepage,News(None,None,None,None),[],name)

	def _findAvailableArticles_(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		This method issue a requests to the website and retrieves all the hotnews
		and some info about them such as time, url, date...

		"""
		articleslist = []
		data = requests.get(self.homepage+"/notizie-ultima-ora/index.shtml").content
		page = BeautifulSoup(data,"html.parser")

		articles = page.find("ul",attrs={"class" : "listing-content"})
		articles = page.findAll("li",attrs={"class" : "listing-item"})
		for article in articles:
			try:
				art_url = article.findAll("a",href=True)[2]['href']
			except:
				art_url = article.findAll("a",href=True)[1]['href']
			art_date = article.find("span",attrs={"class" : "news-date"}).text
			art_time = article.find("span",attrs={"class" : "news-time"}).text
			art_title= article.find("h5",attrs={"class" : "news-title"}).text
			art_category = article.find("span",attrs={"class" : "news-cat"}).text.lower()

			art_full = News(url = self.homepage+art_url,date = art_date,time = art_time,title = art_title,source = self.homepage,source_name = self.websitename,category=art_category)
			articleslist.append(art_full)
		self._articles = articleslist

	def getLastNews(self):
		"""

		Params: None
		Returns: News (Object)
	
		This method check whether if the last news is different from the 
		one scraped now, if it is, returns this one instead of
		the lastNews, and update that one

		"""
		tmp = self.getArticle(0)			# Get the last one
		if self._lastNews.equals(tmp):		# If it's the last stored one
			return None						# Return none
		self._lastNews = tmp				# Else set the last stored one to this one
		return self._lastNews				# Return it
