# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CareerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    fee = scrapy.Field()
    nearest_station = scrapy.Field()
    contract = scrapy.Field()
    language = scrapy.Field()
    skill = scrapy.Field()
    job_content = scrapy.Field()

