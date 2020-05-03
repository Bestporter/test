#ip伪装

import scrapy
from scrapy import signals
import requests
import json
import random
from dangdang.settings import proxies
class ProxyMiddleware(object):
    # global proxies = []
    def fresh(self):
        #高匿 https代理
        r = requests.get('http://127.0.0.1:8000/?types=0&protocol=0')
        ip_ports = json.loads(r.text)
        r = requests.get('http://127.0.0.1:8000/?types=0&protocol=2')
        if json.loads(r.text):
            ip_ports.extend(json.loads(r.text))
        r = requests.get('http://127.0.0.1:8000/?types=1&protocol=0')
        if json.loads(r.text):
            ip_ports.extend(json.loads(r.text))
        r = requests.get('http://127.0.0.1:8000/?types=1&protocol=2')
        if json.loads(r.text):
            ip_ports.extend(json.loads(r.text))
        for i in ip_ports:
            ip = i[0]
            port = i[1]
            proxy='http://%s:%s' % (ip, port)
            proxies.append(proxy)
        r = requests.get('http://127.0.0.1:8000/?types=0&protocol=1')
        ip_ports = json.loads(r.text)
        r = requests.get('http://127.0.0.1:8000/?types=1&protocol=1')
        if json.loads(r.text):
            ip_ports.extend(json.loads(r.text))
        for i in ip_ports:
            ip = i[0]
            port = i[1]
            proxy = 'https://%s:%s' % (ip, port)
            # ip = proxy.split(':')[1].replace('//', '')
            # print(ip+"test\n")
            proxies.append(proxy)
        print(proxies)
    def process_request(self,request,spider):
        # proxies = self.get_proxy()
        if(len(proxies) < 10):
            self.fresh()
        request.meta['proxy'] = random.choice(proxies)
        print(request.meta['proxy'])