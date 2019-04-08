#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .skeletons.news import News
from .skeletons.source import Source
import requests
from bs4 import BeautifulSoup

class Adnkronos(Source):
	def __init__(self):
		homepage = "http://www.adnkronos.com/"
		name = "Adnkronos"
		Source.__init__(self,homepage,News(None,None,None,None),[],name)

	def __getCategory__(self,url):
		url = url.split("/")
		if url[3] != "sport" and url[3]:
			return url[4]
		return url[3]

	def __findAvailableArticles__(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		This method issue a requests to the website and retrieves all the hotnews
		and some info about them such as time, url, date...

		"""
		articleslist = []
		data = requests.get(self.homepage).content
		page = BeautifulSoup(data,"html.parser")
		articles = page.find("ul",{"class":"bxslider_news_tiker"})
		try:
			articles = articles.findAll("li")
		except:
			return

		for article in articles:
			art_url = article.find("a",href=True)['href']
			art_date = None
			art_time = article.findAll("span")[0].text
			art_title= article.findAll("span")[1].text.replace("- ","",1)
			art_category = self.__getCategory__(art_url)	# Attempt to guess category from url
			
			art_full = News(url = art_url,date = art_date,time = art_time,title = art_title,source = self.homepage,source_name = self.websitename,category=art_category)
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
		self.__findAvailableArticles__()	# Updates the list of the articles
		tmp = self.getArticle(0)			# Get the last one
		if self._lastNews.equals(tmp):		# If it's the last stored one
			return None						# Return none
		self._lastNews = tmp				# Else set the last stored one to this one
		return self._lastNews				# Return it
