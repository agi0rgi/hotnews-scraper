#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .skeletons.news import News
from .skeletons.source import Source
import requests
from bs4 import BeautifulSoup

class Ansa(Source):
	def __init__(self):
		homepage = "http://www.ansa.it"
		name = "Ansa"
		Source.__init__(self,homepage,News(None,None,None,None),[],name)


	def __getCategory__(self,data):
		txt = data.find("script").text
		txt = txt.split("(")
		tags = txt[1]
		tags = tags.replace('"',"").split(",")
		try:
			return tags[0].lower()
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
		data = requests.get(self.homepage+"/sito/notizie/topnews/index.shtml").content
		page = BeautifulSoup(data,"html.parser")

		articles = page.find("div",attrs={"class" : "span6 pp-column pull-right"})
		articles = articles.findAll("article",attrs={"class" : "news small"})

		for article in articles:
			art_url = article.find("a",href=True)['href']
			art_date = article.find("em").text.replace("-","")
			art_time = article.find("span").text.replace("-","")
			art_title= article.find("h3",attrs={"class" : "news-title"}).text
			art_category = self.__getCategory__(article)
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
