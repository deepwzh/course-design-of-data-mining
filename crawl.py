import requests
from lxml import etree

url = 'https://cn.vjudge.net/contest/249239#rank'
html = requests.get(url).text

selector = etree.HTML(html)
links = selector.xpath('//*[@id="contest-rank-table"]//tr')
print(links)