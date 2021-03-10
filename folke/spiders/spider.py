import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FolkeItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FolkeSpider(scrapy.Spider):
	name = 'folke'
	start_urls = ['https://folkesparekassen.dk/om-os/nyheder']

	def parse(self, response):
		post_links = response.xpath('//a[@class="heading2"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="layoutcolumn"]//div[@class="layoutbox section"]//div[@class="vdcontent"]/text()').get()
		title = response.xpath('//span[@class="heading1"]/text()').get()
		content = response.xpath('//div[@id="layout51sub1mergefield15"]//text()[not (ancestor::span[@class="vdlabel"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FolkeItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
