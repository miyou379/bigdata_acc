import regex
from bs4 import BeautifulSoup as bs
import urllib.request as urlreq
req = urlreq.Request(url = "https://www.baidu.com/", headers = { "User-Agent":
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" })
got = urlreq.urlopen(req).read() ## http get 
obj = bs(got, 'html.parser') ## parse to bs4 object
print(type(obj))
print(obj.decode()[:500])

## Link
digest = obj.find_all("div", attrs = {"class": "hot-desc_1m_jR large_nSuFU"})
links = [i.a for i in digest]
# print(type(links))
links = [i.get("href") for i in links]
print(len(links), type(links), links)