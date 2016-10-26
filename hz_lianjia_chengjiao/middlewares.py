#!/usr/bin/env python
# coding=utf-8


from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class ShLianJiaUserAgent(UserAgentMiddleware):
    agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0"

    def process_request(self, request, spider):
        request.headers.setdefault("User-Agent", self.agent)
