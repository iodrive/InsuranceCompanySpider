# encoding = utf-8
'''
spider_main.py 上面爬虫流程图中的[调度器]
面向对象写法，调度器负责循环从 UrlManager 获取爬取链接，然后交给 HtmlDownLoader 下载，然后把下载内容交给 HtmlParser 解析，然后把有价值数据输出给 HtmlOutput 进行应用。
'''
import html_downloader
import html_parser
import url_manager
import random
import json
from proxy import Proxy
import time
from http import cookiejar
from urllib import request
import requests

def requests_headers():
    head_connection = ['Keep-Alive']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    #header 为随机产生一套由上边信息的header文件
    header = {
        'Connection':head_connection[random.randrange(0,len(head_connection))],
        'Accept':head_accept[0],
        'Accept-Language':head_accept_language[random.randrange(0,len(head_accept_language))],
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))],
    }
    print('headers.py connection Success!')
    return header #返回值为 header这个字典


class SpiderMain(object):
    def __init__(self):
        self.urlmanager = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.headers = requests_headers()
        self.pro = Proxy('proxy.txt')
        self.proxy = self.pro.get_proxy()
        self.cookie = {'acw_tc': '65c86a0b15537426887978636e5dbbddc9b5401cb8db54fb4cf708596abf28', 'JSESSIONID': '97691AC0C04A7B3B212F3EE77326051B', '_pk_ses.6.1152': '1', '_pk_id.6.1152': 'aa02bb1c2f496b3c.1553742691.2.1553773020.1553770374.', 'SERVERID': '43400b66263d4951d5822515ff6d5921|1553773018|1553770371'}

    def login(self, login_url, return_url, sess):
        pro = Proxy('proxy.txt')
        username = '17714955966'
        password = 't6pbylpr'
        formash = '58FF9E339A'
        backurl = 'https%253A%252F%252Fdb.yaozh.com%252Fhmap'
        logindata = {"username": username, "pwd": password, "formhash": formash, "backurl": backurl}

        header = requests_headers()
        login = sess.post(login_url, data=logindata, headers=header, verify=False)
        cookie = login.cookies
        header["Referer"] = "http://icid.iachina.cn/?columnid_url=201509301401"
        response = sess.get(return_url, headers=header, proxies={"https:": pro.get_proxy()}, verify=False, cookies=cookie)
        return response.text


    def craw(self, root_url, sess):
        companys = []
        pro = Proxy('proxy.txt')
        html_content = self.downloader.download(root_url, retry_count=3, headers=requests_headers(),
                                                proxy=pro.get_proxy(), sess=sess, cookie=self.cookie)
        types, infos = self.parser.get_infos(root_url, html_content)
        for i in range(len(infos)):
            url = "http://icid.iachina.cn/front/getCompanyInfos.do?columnid=" + infos[i][0] + "&informationno=" + infos[i][1] + "&attr=" + infos[i][2]
            inside_html_content = self.downloader.download(url, retry_count=3, headers=requests_headers(),
                                                proxy=pro.get_proxy(), sess=sess)
            company = self.parser.get_data(url, inside_html_content)
            company['叶子结点栏目名称'] = types[i]
            print(company)
            companys.append(company)

        return companys


if __name__ == "__main__":

    rootUrl = "http://icid.iachina.cn/front/getAllInfosByCid.do?columnid=201509301401"
    spider = SpiderMain()
    sess = requests.session()
    sess.trust_env = False
    companys = spider.craw(rootUrl, sess)
    with open('company.json', 'w', encoding='utf-8') as fp:
        fp.write((json.dumps(companys)))
        fp.write('\n')
        fp.close()
