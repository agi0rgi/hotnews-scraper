#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .modules import tgcom,ansa,corriere,tiscali,adnkronos,rainews
import time,logging
sources = []

logging.basicConfig(format='%(asctime)s -    %(levelname)s    - %(message)s', level=logging.INFO)

sources.append(tgcom.Tgcom())
sources.append(ansa.Ansa())
sources.append(corriere.Corriere())
sources.append(tiscali.Tiscali())
sources.append(adnkronos.Adnkronos())
sources.append(rainews.Rainews())

class NewsScraper():
	def __init__(self,delay = 60):
		self.delay = delay

	def getAllNews(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		This method get all the scraped articles from the
		sources modules, and returns a list of all the news

		"""
		news = []
		for source in sources:
			found = source.getAvailableArticles()
			if found != None:
				news.extend(found)
			else:
				logging.warning("Missing one news from %s." % (source.websitename))
		return news

	def printAllNews(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		This method print every news found with getAllNews method

		"""
		for news in self.getAllNews():
			print(news.getNews()+"\n")

	def getAllRawNews(self):
		"""

		Params: None
		Returns: List dictionaries
	
		Returns dictionaries containing news information
		like:
		{
			"url" : "link",	
			"time": "10:00";
			"date": "1 Aug";//That depends from the sources
			"title": "Title";
			"source": "link to source website";
			"source_name": "source's name";
		}
		"""
		raw = []
		for item in self.getAllNews():
			raw.append(item.getRawNews())
		return raw

	def getLastNews(self):
		"""

		Params: None
		Returns: List of News (List of Objects)
	
		Gets the last news from every sources' module

		"""
		news = []
		for source in sources:
			found = source.getLastNews()
			if found != None:
				news.append(found)
			else:
				logging.info("No new news on %s." % (source.websitename))
		return news

	def getLastRawNews(self,rawnewses=[]):
		"""

		Params: rawnewses(Lists)
		Returns: List dictionaries
	
		Returns dictionaries containing news information
		like:
		{
			"url" : "link",	
			"time": "10:00";
			"date": "1 Aug";//That depends from the sources
			"title": "Title";
			"source": "link to source website";
			"source_name": "source's name";
		}
		"""
		raw = []
		for item in self.getLastNews():
		    if rawnewses:
		        for tmp in rawnewses:
		            if not item.equals(tmp):
			            raw.append(item.getRawNews())
			else:
			    raw.append(item.getRawNews())
		return raw


	def printLastNews(self):
		"""

		Params: None
		Returns: Nothing
	
		Prints all the last news

		"""
		for item in self.getLastNews():
			print(item.getNews()+"\n")

	def loop(self):
		"""

		Params: None
		Returns: Nothing
	
		Loops the programs, and checks for news every self.delay seconds

		"""
		while True:
			self.printLastNews()
			logging.info("Sleeping %s seconds before next update." % self.delay)
			time.sleep(self.delay)
