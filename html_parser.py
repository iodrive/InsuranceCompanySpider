'''
html_parser.py 上面爬虫流程图中的[解析器]
负责对下载器下载下来的网页内容进行解析，解析规则就是我们自己定义的感兴趣的内容，这里我们只分析网页后解析出 url、title、content，其他的不关心，解析好的数据通过字典返回。
'''
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html_downloader

class HtmlParser(object):
    dowmloader = html_downloader.HtmlDownloader()
    def parse(self, url, content, html_encode="utf-8"):
        if url is None or content is None:
            return
        soup = BeautifulSoup(content, "lxml")
        new_data = self.__get_infos(url, soup)
        return new_data

    def get_new_urls(self, url, content):
        soup = BeautifulSoup(content, "lxml")
        new_urls = set()
        hospital_node = soup.find_all('ul', class_='hos_ul')
        sub_soup = BeautifulSoup(str(hospital_node), 'lxml')
        links = sub_soup.find_all("a")
        for link in links:
            url_path = link['href']
            new_url = urljoin(url, url_path)
            new_urls.add(new_url)
        return new_urls

    def get_data(self, url, content, html_encode="utf-8"):
        '''
        解析具体公司html 获得data
        :param url:
        :param content:
        :param html_encode:
        :return:
        '''
        if url is None or content is None:
            return
        soup = BeautifulSoup(content, "lxml")

        company = {}
        ps = soup.find_all('p', class_='kk')
        company['披露机构全称'] = str(ps[0].string).strip()
        company['披露机构简称'] = str(ps[1].string).strip()
        company['经营互联网保险业务的网站名称'] = str(ps[2].string).strip()
        company['经营互联网保险业务的网站地址'] = str(ps[3].string).strip()
        company['经营互联网保险业务的APP名称'] = str(ps[4].string).strip()
        company['经营互联网保险业务的微信公众号名称'] = str(ps[5].string).strip()
        company['客户服务及消费者投诉电话'] = str(ps[6].string).strip()
        company['机构信息披露网站地址'] = str(ps[7].string).strip()
        return company



    def get_infos(self, url, content, html_encode="utf-8"):
        '''
        解析html 获得infos
        :param url:
        :param soup:
        :return:
        '''
        if url is None or content is None:
            return
        soup = BeautifulSoup(content, "lxml")

        infos = []
        types = []

        table_node = soup.find_all('li')
        sub_soup = BeautifulSoup(str(table_node), 'lxml')

        lis = sub_soup.find_all('li')
        for li in lis:
            info = []
            li_soup = BeautifulSoup(str(li), 'lxml')
            strinfo = str(li_soup.a['onclick']).split('\'')
            info.append(strinfo[5])
            info.append(strinfo[1])
            info.append(strinfo[3])
            infos.append(info)
            type = str(li_soup.p.string).strip()
            types.append(type)

        return types, infos