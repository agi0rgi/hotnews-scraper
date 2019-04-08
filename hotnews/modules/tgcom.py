#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .skeletons.news import News
from .skeletons.source import Source
import requests
from bs4 import BeautifulSoup

class Tgcom(Source):
	def __init__(self):
		homepage = "http://www.tgcom24.mediaset.it"
		name = "Tgcom24"
		Source.__init__(self,homepage,News(None,None,None,None),[],name)

	def __getCategory__(self,url):
		try:
			return url.split("/")[1]	
		except:
			return "ultimora"

	def _findAvailableArticles_(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		This method issue a requests to the website and retrieves all the hotnews
		and some info about them such as time, url, date...

		"""
		articleslist = []
		data = requests.get(self.homepage+"/ultimissima/oraxora.shtml").content
		page = BeautifulSoup(data,"html.parser")

		articles = page.find("ul",attrs={"class" : "rt rt__hour"})
		art_date = articles.findAll("time")[0].text					# Same for all the articles
		articles = articles.findAll("li")
		for article in articles:
			art_url = article.find("a",href=True)['href']
			art_time = article.find("time").text
			art_title= article.find("h3").text.strip()
			art_category = self.__getCategory__(art_url)

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
