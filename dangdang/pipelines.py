# -*- coding: utf-8 -*-
import pymongo
from dangdang.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        item['star'] = item['star'].replace('width: ','').replace(';','')
        #注：二手书没有出版社
        # if item['press']:
        #     item['press'] = item['press'].replace(' /','')
        if item['comment']:
            item['comment'] = item['comment'].replace('条评论','')
        if item['pubdate']:
            item['pubdate'] = item['pubdate'].replace(' /','')
        item['book_name'] = item['book_name'].strip()
        data = dict(item)
        # self.post.insert(data)
        try:
            self.post.insert(data)
            print('插入书籍url%s' % (item['book_name']))
        except Exception:
            print("%s存在了,跳过" % item["_id"])
        return item
