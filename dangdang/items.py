# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #书名
    book_name = scrapy.Field();
    #价格
    price = scrapy.Field();
    #作者
    author = scrapy.Field();
    #出版社
    press = scrapy.Field();
    #星级
    star = scrapy.Field();
    #评论数
    comment = scrapy.Field();
    #评论url
    comment_url = scrapy.Field();
    #商家
    business = scrapy.Field();
    #出版日期
    pubdate = scrapy.Field();
    #书籍详情页
    _id = scrapy.Field();



