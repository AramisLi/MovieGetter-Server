# -*- coding: utf-8 -*-
# create by Aramis
import re
import time
import sys

import requests
from scrapy.selector import Selector
from module_mysql import MysqlClient

sys.path.append('../')
from utils import woff2number

URL_TAG0 = 'http://maoyan.com/board/7'
URL_TAG1 = 'http://maoyan.com/board/6'
URL_TAG2 = 'http://maoyan.com/board/1'
URL_TAG3 = 'http://maoyan.com/board/2'
URL_TAG4 = 'http://maoyan.com/board/4'
URL_DETAIL = 'http://maoyan.com/films/{id}'

HEADER = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}


class MyController:
    urls = [URL_TAG0, URL_TAG1, URL_TAG2, URL_TAG3, URL_TAG4]
    switch_tag_name = {
        0: '热映口碑榜',
        1: '最受期待榜',
        2: '国内票房榜',
        3: '北美票房榜',
        4: 'TOP100榜',
    }

    def __init__(self):
        self.client = MysqlClient()

    def crawl(self):
        for i, item in enumerate(self.urls):
            self._crawl(item, i)
            time.sleep(2)

    def _crawl(self, url, tag: int):
        print('开始爬取', url)
        res = requests.get(url=url, headers=HEADER)
        html = res.text

        if res and res.status_code == 200:
            print('访问成功')
            selector = Selector(text=html)
            font_resource = self._get_font(url, html, selector)
            wrappers = selector.xpath('//div[@class="container"]//div[@class="main"]//dd').extract()
            update_time = selector.xpath(
                '//div[@id="app"]//div[@class="main"]/p[@class="update-time"]/text()').extract_first()
            for index, i in enumerate(wrappers):
                movie = dict()
                # print(i)
                selector2 = Selector(text=i.__str__())
                movie['movie_name'] = selector2.xpath('//a[@class="image-link"]/@title').extract_first()
                href = selector2.xpath('//a[@class="image-link"]/@href').extract_first()
                # href=''
                movie['movie_id'] = int(href[href.rindex('/') + 1:len(href)])
                movie['movie_year'] = selector2.xpath('//p[@class="releasetime"]/text()').extract_first()
                movie['actors'] = selector2.xpath('//p[@class="star"]/text()').extract_first().strip()
                movie['score'] = ''.join(selector2.xpath('//p[@class="score"]/i/text()').extract())
                movie['ranking'] = int(selector2.xpath('//i[contains(@class,"board-index")]/text()').extract_first())
                movie['cover_image'] = selector2.xpath('//img[@class="board-img"]/@data-src').extract_first()
                if '@' in movie['cover_image']:
                    movie['cover_image'] = movie['cover_image'][0:movie['cover_image'].index('@')]
                movie['tag'] = tag
                movie['update_time'] = update_time

                self._merge_font_res(url, font_resource, movie, index)
                self.crawl_detail(movie)

            # top100
            if tag == 4:
                time.sleep(1)
                if 'offset' in url:
                    num = int(url[url.rindex('=') + 1:len(url)])
                    if num >= 90:
                        return
                    next_url = url[0:url.rindex('=') + 1] + str(num + 10)
                else:
                    next_url = url + '?offset=10'
                self._crawl(next_url, tag)
        else:
            print('访问出错', url)

    def _merge_font_res(self, url: str, res: tuple, d: dict, index: int):
        if res:
            s = {
                URL_TAG2: ('boxoffice', 'boxoffice_all'),
                URL_TAG1: ('wanna_watch', 'wanna_watch_all'),
                URL_TAG3: ('boxoffice_lastweek', 'boxoffice_all'),
            }
            t = s.get(url, None)
            if t:
                l1 = res[0]
                l2 = res[1]
                if index < len(l1):
                    d[t[0]] = l1[index]
                if index < len(l2):
                    d[t[1]] = l2[index]

    def _get_font(self, url, html, selector):
        if url == URL_TAG1 or url == URL_TAG2 or url == URL_TAG3:
            font_url = 'http:' + re.findall(re.compile('//vfile.*?.woff'), html)[0]
            print('字体地址', font_url)
            woff2number.save_font(font_url)
            s = {
                # class,filter
                URL_TAG2: ('realtime', '实时票房', 'total-boxoffice', '总票房'),
                URL_TAG1: ('month-wish', '本月新增想看', 'total-wish', '总想看'),
                URL_TAG3: ('realtime', '上周末票房', 'total-boxoffice', '总票房'),
            }
            t = s.get(url, None)

            def get_l(tt: tuple):
                class_s = tt[0]
                filter_s = tt[1]
                realtimes_str = re.findall(re.compile('{class_s}.*?stonefont\">(.*?)</span>'.format(class_s=class_s)),
                                           html)
                realtimes_c = [i.strip() for i in
                               selector.xpath('//p[@class="{class_s}"]/text()'.format(class_s=class_s)).extract() if
                               '{filter_s}'.format(filter_s=filter_s) not in i]
                realtimes1 = woff2number.parse_list2num_str(realtimes_str)
                realtimes = [item + realtimes_c[i] if i < len(realtimes_c) else item for i, item in
                             enumerate(realtimes1)]
                print(filter_s, realtimes)
                return realtimes

            if t:
                return get_l((t[0], t[1])), get_l((t[2], t[3]))

    def crawl_detail(self, movie: dict):
        movie_id = movie['movie_id']
        detail_url = URL_DETAIL.format(id=movie_id)
        res = requests.get(url=detail_url, headers=HEADER)
        if res and res.status_code == 200:
            selector = Selector(text=res.text)
            _description = selector.xpath('//meta[@name="description"]/@content').extract_first()
            movie['description'] = _description[_description.index(':') + 1:len(_description)]
            images = selector.xpath('//div[@class="module"]/div[@class="mod-content"]//img/@data-src').extract()
            _images = ''
            for i in images:
                if '@' in i:
                    _images += i[0:i.index('@')]
                else:
                    _images += i
                    _images += ','
            if _images:
                _images = _images[0:len(_images) - 1]
            movie['images'] = _images

            self._save(movie)

        else:
            print('访问详情出错', detail_url, res.status_code, res.text)

    def _save(self, d: dict):
        d['sync_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        d['tag_name'] = self.switch_tag_name.get(d['tag'], 'none')
        keys = ','.join(d.keys())
        values = ','.join('\"{i}\"'.format(i=i) if type(i) == str else str(i) for i in d.values())
        duplicate = ','.join(
            ['{k}={v}'.format(k=k, v='\"{v}\"'.format(v=v) if type(v) == str else str(v)) for k, v in d.items()])
        sql = 'insert into maoyan_board({keys}) values ({valuess}) ON DUPLICATE KEY UPDATE {duplicate};'.format(
            keys=keys, valuess=values, duplicate=duplicate)
        # print(sql)
        self.client.save(sql)

    def get_data(self, tag, page_num, page_size):
        print('tag', tag, 'page_num', page_num, 'page_size', page_size)
        return self.client.get_movie_board_data(tag=tag, limit=page_size, offset=int(page_num) * int(page_size))


if __name__ == '__main__':
    controller = MyController()
    # controller._crawl(URL_TAG1, 1)
    controller.crawl()
    # r = controller.get_data('0', '0', '10')
    # print(r)
