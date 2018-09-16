# -*- coding: utf-8 -*-
import json

import scrapy

from ZhihuScrapy.items import ZhihuItem


class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 爬取的起点（第一个用户url_token）
    start_user = 'chai-sheng-mang'

    # 用户基本信息的请求url
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # 以上url的相关属性（即include位置内容）
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 用户所关注列表的url和相关属性
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 起始请求作用，Requests如果携带dont_filter=True，则start_urls中的 URL 在首次请求时不会加入过滤列表中
    def start_requests(self):
        yield scrapy.Request(
            url=self.follow_url.format(user=self.start_user, include=self.follow_query, offset=0, limit=20),
            callback=self.follow_parse)
        yield scrapy.Request(url=self.user_url.format(user=self.start_user, include=self.user_query),
                             callback=self.user_parse)

    def follow_parse(self, response):
        # get source code of the web in json format
        result = response.text
        # Decode JSON data and convert it to data type of thePython field
        follows = json.loads(result)
        # Judge whether 'data' is in the keys of follows
        if 'data' in follows.keys():
            # traverse all data and get the url_token of users
            for follow in follows.get('data'):
                url_token = follow.get('url_token')
                yield scrapy.Request(url=self.user_url.format(user=url_token, include=self.user_query),
                                     callback=self.user_parse)
        # Judge whether to turn pages
        if 'paging' in follows.keys() and follows.get('paging').get('is_end') == False:
            next_url = follows.get('paging').get('next')
            yield scrapy.Request(url=next_url, callback=self.follow_parse)

    def user_parse(self, response):
        # get source code of the web in json format
        result = response.text
        # Decode JSON data and convert it to data type of thePython field
        infos = json.loads(result)

        # Define item
        item = ZhihuItem()
        # circulate all keys of the infos
        for info in infos.keys():
            # Judge whether info is the list of field
            if info in item.fields:
                # If 'yes' ,get it a value
                item[info] = infos.get(info)
        yield item

        # Get this person`s following list
        yield scrapy.Request(
            url=self.follow_url.format(user=item['url_token'], include=self.follow_query, offset=0, limit=20),
            callback=self.follow_parse)
