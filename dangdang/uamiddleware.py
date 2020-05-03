#user-agent下载中间件
import scrapy
from scrapy import signals
import random
from dangdang.settings import UAPOOL
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
class Uamiddleware(UserAgentMiddleware):
    def __init__(self,user_agent):
        self.user_agent = user_agent;
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         ua = crawler.settings.get('UAPOOL')
    #     )
    def process_request(self, request, spider):
        agent = random.choice(UAPOOL)
        request.headers['User-Agent'] = agent