import requests
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
url = 'http://category.dangdang.com/'
headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36"}
response = requests.get(url,headers=headers)
response1 = HtmlResponse(url='http://category.dangdang.com/',body=response.text,encoding='utf8')
#print(response1.text)
le = LinkExtractor()
links = le.extract_links(response1)
restrict_xpaths = LinkExtractor(restrict_xpaths='//div[@id ="floor_1"]//div[@class="classify_kind_name"]')
links_restrict_xpaths = restrict_xpaths.extract_links(response1)
urls = [link_restrict_xpaths.url for link_restrict_xpaths in links_restrict_xpaths]
with open('../dangdang/spiders/urls.txt','w') as file:
    for i in urls:
        file.write(i+'\n')