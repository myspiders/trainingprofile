# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()#标题
    time1 = scrapy.Field()#新闻发布时间
    text= scrapy.Field()#新闻文本内容
    reads= scrapy.Field()#阅读总量
    stck = scrapy.Field()#证券代码
    origin = scrapy.Field()#新闻来源
    cri_counts = scrapy.Field()#评论总数
    nickname=scrapy.Field()#评论昵称
    time2=scrapy.Field()#评论时间
    content=scrapy.Field()#评论内容
    newsid=scrapy.Field()#新闻id
    pass
