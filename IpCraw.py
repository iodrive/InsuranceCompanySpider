from bs4 import BeautifulSoup
import requests
import re
from lxml import etree

def get_xici_proxy(page_no):
    url = "https://www.xicidaili.com/nn/{}".format(page_no)
    headers = {"User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
    r = requests.get(url, verify=False, headers=headers)
    content = r.content.decode("utf-8")
    root = etree.HTML(content)
    tr_nodes = root.xpath('.//table[@id="ip_list"]/tr')[1:]
    result = []
    for tr_node in tr_nodes:
        td_nodes = tr_node.xpath('./td')
        ip = td_nodes[1].text
        port = td_nodes[2].text
        proxy_type = td_nodes[4].text
        proto = td_nodes[5].text
        proxy = "{}://{}:{}".format(proto.lower(), ip, port)
        uptime = td_nodes[8].text
        if proxy_type == "高匿" and proto.lower() == "https":
            result.append(proxy)
    return result

def test_proxy(proxy):
    https_url = "https://book.douban.com/tag/SQL?start=20&type=T"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    try:
        proxies = {"https": proxy}
        r = requests.get(https_url, headers=headers, verify=False, proxies=proxies, timeout=10)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        items = root.xpath('.//li[@class="subject-item"]')

        print(r.status_code)
        if r.status_code == 200 and len(items) == 20:
            print(proxy)
            return True
        return False
    except Exception as e:
        msg = str(e)
        return False

if __name__ == '__main__':
    res = get_xici_proxy(7)
    print(res)
    fp = open('proxy.txt', 'a')
    for proxy in res:
        if test_proxy(proxy):
            fp.write(str(proxy))


