#!/usr/bin/env python
# coding=utf-8

import logging
import scrapy
from sh_lianjia_chengjiao.items import HZLianjiaChengjiaoItem


class HZLianJiacrawler(scrapy.Spider):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="./log.log",
        filemode='w',
    )

    all_url = set([])
    name = "hz_lianjia"
    start_urls = (
        'http://hz.lianjia.com/chengjiao/',
    )

    '''
    def start_requests(self):
        yield scrapy.Request('https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fhz.lianjia.com%2F',
                                      meta={'cookiejar': 1},
                                      callback=self.login_index
                                      )

    def login_index(self, response):
        print "url: " + response.url
        lt = response.xpath("//input[@name='lt']/@value").extract_first()
        execution = response.xpath("//input[@name='execution']/@value").extract_first()
        _eventId = response.xpath("//input[@name='_eventId']/@value").extract_first()

        print "lt: " + lt
        print "execution: " + execution
        print "_eventId: " + _eventId

        yield scrapy.FormRequest.from_response(response,
            meta={'cookiejar': response.meta['cookiejar']},
            formdata={
            'redirect':'',
            'verifyCode':'',
            'username': '18729572150',
            'password': '911027',
            'lt': lt,
            'execution': execution,
            '_eventId': _eventId,
            },  callback=self.go_to_parse
       )

    def go_to_parse(self, response):
        chengjiao_url = response.urljoin("/chengjiao")
        print 'chengjiao_url: ' + chengjiao_url
        yield scrapy.Request(chengjiao_url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse)
    '''
    def parse(self, response):
        print response.url
        logging.debug("start a new hub!")
        # area_list = response.xpath('//div[@class="option-list gio_district"]/a/@href').extract()[1:]
        area_list = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for area_url in area_list:
            complete_area_url = response.urljoin(area_url)
            logging.debug("complete_area_url: " + complete_area_url)
            yield scrapy.Request(complete_area_url, callback=self.get_each_page)
    '''
    def get_sub_area(self, response):
        # sub_area_list = response.xpath('//div[@class="option-list sub-option-list gio_plate"]/a/@href').extract()[1:]
        sub_area_list = response.xpath('//div[@class="option-list sub-option-list gio_plate"]/a/@href').extract()[1:]
        for sub_area in sub_area_list:
            sub_area_url = response.urljoin(sub_area)
            logging.debug("sub_area_url: " + sub_area_url)
            yield scrapy.Request(sub_area_url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.get_each_house)
    '''
    def get_each_page(self, response):
        all_house_num = response.xpath('//div[@class="total fl"]/span/text()').extract_first()
        house_num_per_page = len(response.xpath('//ul[@class="listContent"]/li'))
        if not house_num_per_page:
            return
        page_num = int(all_house_num) / int(house_num_per_page)
        if int(all_house_num) % int(house_num_per_page):
            page_num += 1
        for i in range(1, page_num+1):
            next_url = response.url + 'pg' + str(i) + '/'
            print 'next_url: ' + next_url
            yield scrapy.Request(next_url, callback=self.get_each_house)

    def get_each_house(self, response):
        house_list = response.xpath('//ul[@class="listContent"]/li/a/@href').extract()
        for house in house_list:
            print "housed_detail_url: " + house
            yield scrapy.Request(house, callback=self.get_house_detail)

    def get_house_detail(self, response):
        # print "if i am here:\n"
        # 简单的去重复
        house_detail_url = response.url
        logging.debug("house_detail_url" + house_detail_url)
        if response.url not in self.all_url:
            self.all_url.add(response.url)
        else:
            return
        item = HZLianjiaChengjiaoItem()

        # item['decorate_status'] = all_data_div.xpath("table/tr[3]/td[1]/text()").re_first("\w+")
        item['total_floor'] = response.xpath('//div[@class="msg"]/span[1]/text()').extract_first()
        item['house_orientation'] = response.xpath('//div[@class="msg"]/span[2]/label/text()').extract_first()
        item['total_price'] = response.xpath('//div[@class="price"]/span/i/text()').extract_first()
        item['floor'] = response.xpath('//div[@class="msg"]/span[1]/text()').extract_first()
        item['unit_price'] = response.xpath('//div[@class="price"]/b/text()').extract_first()
        item['house_year'] = response.xpath('//div[@class="msg"]/span[3]/text()').extract_first()
        item['house_structure'] = response.xpath('//div[@class="msg"]/span[1]/label/text()').extract()[0]
        item['name'] = response.xpath('//div[@class="info fr"]/p[1]/a[1]/text()').extract_first()
        item['idx'] = response.xpath('//div[@class="info fr"]/p[1]/a[1]/text()').extract_first()
        item['area'] = response.xpath('//div[@class="msg"]/span[3]/label/text()').extract_first()
        item['xiaoqu_id'] = response.xpath('//div[@class="info fr"]/p[1]/a[1]/text()').extract_first()
        item['deal_time'] = response.xpath('//div[@class="wrapper"]/span/text()').re_first('\d*\.\d*.\d*')
        item['url'] = response.url
        item['datatype'] = "chengjiao_detail"
        item['province'] = "杭州"
        item['site'] = "lianjia"
        item['house_type'] = "na"
        item['city'] = "杭州"
        item['pub_time'] = "na"
        item['deal_status'] = "0"
        yield item

