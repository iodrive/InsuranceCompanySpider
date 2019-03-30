
'''
url_manager.py 上面爬虫流程图中的[URL 管理器]
负责管理深度 URL 链接和去重等机制。
'''


class UrlManager(object):
    def __init__(self):
        self.new_url = set()
        self.used_url = set()

    def add_new_url(self, url):
        if url is None:
            return
        else:
            if url not in self.new_url and url not in self.used_url:
                self.new_url.add(url)

    def add_new_urls(self, urls):
        if urls is None or not len(urls):
            return
        else:
            for url in urls:
                self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_url) > 0

    def get_new_url(self):
        tmp_url = self.new_url.pop()
        self.used_url.add(tmp_url)
        return tmp_url
