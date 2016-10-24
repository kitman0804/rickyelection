import requests
from lxml import html
from time import sleep

# header
h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}


# Data Scraper
def read_html(url, headers=h, sleep_seconds=10):
    try:
        html_page = requests.get(url, headers = headers)
        print("Successfully read %s" % url)
        sleep(sleep_seconds)
    except Exception as e:
        print(e)
        return None
    return html_page.content


html_code = read_html("https://www.rickyelection.hk/zh/policies/")

html_obj = html.fromstring(html_code)

policy = html_obj.xpath("//*[@id='home-political-platform']//a[not (contains(span//text(), '下載全部政綱'))]")
policy = [a.xpath("./@href")[0] for a in policy]
policy = [read_html(href) for href in policy]

articles = [html.fromstring(x) for x in policy]
articles = [[x.xpath("//h1[@class='post-title']//text()"),
             x.xpath("//div[@class='post-entry']//p/text() | //div[@class='post-entry']//h2/text()")]
            for x in articles]
articles = [[x[0][0], "\r\n".join(x[1])] for x in articles]


for i in range(len(articles)):
    f = open("article/article%02.0f_%s.txt" % (i + 1, articles[i][0]), "wb")
    f.write(bytearray(articles[i][1], "utf8"))
    f.close()
    del f

