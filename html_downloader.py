# encoding=utf8
'''
html_downloader.py 上面爬虫流程图中的[下载器]
负责对指定的 URL 网页内容进行下载获取
'''
from urllib import request, error
from http import cookiejar
from urllib.parse import urlparse
import requests


class HtmlDownloader(object):
    def download(self, url, retry_count=3, headers = None, proxy = None, data = None, referer = None, cookie = None, sess = None):
        if url is None:
            return None
        try:
            '''
            req = request.Request(url, headers=headers, data=data)
            cookie = cookiejar.CookieJar()
            cookie_process = request.HTTPCookieProcessor(cookie)
            opener = request.build_opener()
            if proxy:
                proxies = {urlparse(url).scheme: proxy}
                opener.add_handler(request.ProxyHandler(proxies))
            content = opener.open(req).read()
            '''
            resp = sess.get(url, headers=headers, proxies={"https:": proxy}, verify=False, cookies=cookie)
            content = resp.text

        except error.URLError as e:
            print('HtmlDownloader download error:', e.reason)
            content = None
            if retry_count > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:  # 说明是 HTTPError 错误且 HTTP CODE 为 5XX 范围说明是服务器错误，可以尝试再次下载
                    return self.download(url, retry_count-1, headers, proxy, data)
        return content
