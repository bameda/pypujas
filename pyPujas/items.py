# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PypujasItem(scrapy.Item):
    id_puja = scrapy.Field()
    link = scrapy.Field()
    debt = scrapy.Field()
    value = scrapy.Field()
    min_puja = scrapy.Field()
    creditor = scrapy.Field()
    property_type = scrapy.Field()
    property_address = scrapy.Field()
    property_description = scrapy.Field()
    property_town = scrapy.Field()
    property_province = scrapy.Field()
    max_puja = scrapy.Field()
    status = scrapy.Field()
