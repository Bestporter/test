# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
import pymongo
from dangdang.settings import mongo_host,mongo_port

class DangdangspiderSpider(scrapy.Spider):

    def get_urls():
        urls = []
        with open(r'c:\pythonProject\dangdang\dangdang\spiders\urls.txt','r') as file:
            for line in file :
                urls.append(line.strip('\n'))
        print(urls)
        print(len(urls))
        return urls
    #源码：
    '''
    def start_requests(self):
        for url in self.start_urls:
        yield self.make_requests_from_url(url)
    '''
    #从dangdang_url 中提取start_url
    def start_requests(self):
        client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        mydb = client['dangdang_url']
        post = mydb['urls']
        li = post.find()
        for i in li:
            # print(i['_id'])
            yield self.make_requests_from_url(i['_id'])
        client.close()
    #
    # def make_requests_from_url(self, url):
    #     return scrapy.Request(url=url,meta={'download_timeout':20},callback=self.parse)
    name = 'dangdangSpider'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://category.dangdang.com/cp01.01.00.00.00.00.html']
    #get_urls()
    #try first time

    # def make_requests_from_url(self, url):
    #     yield scrapy.Request(url=url,meta={'download_timeout':10},callback=self.parse)

    def parse(self, response):

        #print(response.text)
        tmp = response.xpath("//div[@id='bd']//li[@id]")#选取中商品
        # print(type(tmp))
        print(len(tmp))
        for li in tmp :
            item = DangdangItem()
            item['book_name'] = li.xpath('p[@name]/a/@title').extract_first()
            item['price'] = li.xpath("p[@class='price']/span[@class='search_now_price']/text()").extract_first()
            #print(item['price'])
            item['author'] = li.xpath("p[@class='search_book_author']/span[1]/a[1]/@title").extract_first()
            item['pubdate'] = li.xpath("p[@class='search_book_author']/span[2]/text()").extract_first()
            item['press'] = li.xpath("p[@class='search_book_author']/span[3]/a[1]/@title").extract_first()
            item['star'] = li.xpath("p[@class='search_star_line']/span/span/@style").extract_first()
            item['_id'] = li.xpath("a/@href").extract_first()
            item['comment'] = li.xpath("p[@class='search_star_line']/a/text()").extract_first()  #a/@href可以提取到评论的连接
            item['comment_url'] = li.xpath("p[@class='search_star_line']/a/@href").extract_first()  # a/@href可以提取到评论的连接
            #print(item['comment_url'])
            #print(item['star'],item['book_url'])
            #print(item['author'],item['press'],item['pubdate'])
            yield item
        # next = tmp.xpath("//li[@class='next']/a/@href")
        #print(next)
        # if next:
        #     print("http://category.dangdang.com"+next.extract_first())
        #     yield scrapy.Request("http://category.dangdang.com"+next.extract_first(),callback=self.parse)
       #书名 // li[ @ sku] / p[ @ name]

        #价格//li[@sku]/p[@class='price']/span[@class='search_now_price'] 有折扣的情况下，无折扣饿另说
#作者，出版社//li[@sku]/p[@class='search_book_author']/span/a[1]/@title
#星级//li[@sku]/p[@class='search_star_line']/span/span/@style   width: 90%;
#//li[@sku]/p[@class='search_star_line']/a      1232312条评论  评论数
#//评论网址//li[@sku]/p[@class='search_star_line']/a/@href
#出版日期//li[@sku]/p[@class='search_book_author']/span[2]      /2013-01-01