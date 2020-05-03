import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random
import logging
import time
import requests
from dangdang.settings import proxies

class MyRetryMiddleware(RetryMiddleware):

    logger = logging.getLogger(__name__)

    def delete_proxy(self, proxy):
        print("要处理得代理：",proxy)
        print(type(proxy))
        if proxy in proxies:
            print("正在删除代理")
            # delete proxy from proxies pool
            ip = proxy.split(':')[1].replace('//','')
            r = requests.get('http://127.0.0.1:8000/delete?ip=%s'%ip)
            proxies.remove(proxy)
            self.logger.warning('成功删除代理')
        print("剩余代理数：" ,len(proxies))

    def process_response(self, request, response, spider):
        print('ponse')
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            # time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        print('E')
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(1, 4))
            self.logger.warning('连接异常, 进行重试...')
            return self._retry(request, exception, spider)
#其中_retry方法有如下作用：
# 1、对request.meta中的retry_time进行+1
# 2、将retry_times和max_retry_time进行比较，
# 如果前者小于等于后者，利用copy方法在原来的request上复制一个新request，
 # 并更新其retry_times，并将dont_filter设为True来防止因url重复而被过滤。

