#-*-coding:utf-8-*-  
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from emoji_link_spider import items
import scrapy
from urllib import urlretrieve
import string
import os
import MySQLdb
class MySpider(BaseSpider):
	name = "emoji_link_spider"
	allowed_domains = ["emojipedia.org"]
	start_urls = [
	]
	db = MySQLdb.connect("localhost","root","xc731210","emoji")
	cursor = db.cursor()
	def __init__(self):
		self.start_urls.append("https://emojipedia.org")
	def parse(self,response):
		hxs = HtmlXPathSelector(response)
		links = hxs.xpath('//div[@class="sidebar"]')
		links_categories=links[0].xpath('.//div[@class="block"]')[0].xpath('./ul/li/a/@href').extract()
		categories_text=links[0].xpath('.//div[@class="block"]')[0].xpath('./ul/li/a/text()').extract()
		
		#get the categories in the emoji net
		#and take a new fork for each one 
		for index in range(len(links_categories)):
			links_categories[index] = links_categories[index]
			try:
				os.mkdir('F:\PythonProject\ouput\emoji\\'+categories_text[index])
			except WindowsError:
				print "fork already exist"
			print links_categories[index]
			print categories_text[index]
			url = response.urljoin(links_categories[index])
			yield scrapy.Request(url,meta={'item':categories_text[index]},callback=self.parse_categories)

	def parse_categories(self,response):
		res=HtmlXPathSelector(response)
		links=res.xpath('//div[@class="content"]/ul/li/a/@href').extract()
		links_text=res.xpath('//div[@class="content"]/ul/li/a/text()').extract()
		insert_image = ("INSERT INTO emoji(image)" "VALUES(%s)")
		print "#########################"
		for index in range(len(links)):
			print links[index]	
			data_image = (links_text[index])
			self.cursor.execute(insert_image,data_image)
			self.db.commit()
			try:
				os.mkdir('F:\PythonProject\ouput\emoji\\'+response.meta['item']+'\\'+links_text[index])
			except WindowsError:
				print "fork already exist"
			url = response.urljoin(links[index])
			yield scrapy.Request(url,meta={'item':response.meta['item'],'item2':links_text[index]},callback=self.parse_image)
	
	def parse_image(self,response):
		res=HtmlXPathSelector(response)
		links_text=res.xpath('//ul[@class="vendor-rollout"]/li/div/div/p[@class="version-name"]/a/text()')
		links_image=res.xpath('//ul[@class="vendor-rollout"]/li/div/div/a/img/@data-src')
		print links_image[0].extract()
		# print len(links_image)
		# print len(links_text)
		for index in range(len(links_image)):
			print "downloading"
			try:
				urlretrieve(links_image[index].extract(),'F:\PythonProject\ouput\emoji\\'+response.meta['item']+'\\'+response.meta['item2']+"\\"+links_text[index].extract()+".png")
			except WindowsError:
				print "image already exist"
		print "downed!!!!!"