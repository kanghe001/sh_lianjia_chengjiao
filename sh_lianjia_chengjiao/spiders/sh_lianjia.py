#!/usr/bin/env python
# coding=utf-8

import logging
import scrapy
from sh_lianjia_chengjiao.items import ShLianjiaChengjiaoItem


class ShLianJiacrawler(scrapy.Spider):
    logging.basicConfig(
        format="%(asctime)s %datetime"
    )

    all_url = set([])
    name = "sh_lianjia"
    start_urls = (
        'http://sh.lianjia.com/chengjiao',
    )

    def parse(self, response):
        # area_list = response.xpath('//div[@class="option-list gio_district"]/a/@href').extract()[1:]
        area_list = response.xpath('//div[@class="option-list gio_district"]/a/@href').extract()[1:2]
        for area_url in area_list:
            complete_area_url = response.urljoin(area_url)
            print "complete_area_url: " + complete_area_url
            yield scrapy.Request(complete_area_url, callback=self.get_sub_area)

    def get_sub_area(self, response):
        # sub_area_list = response.xpath('//div[@class="option-list sub-option-list gio_plate"]/a/@href').extract()[1:]
        sub_area_list = response.xpath('//div[@class="option-list sub-option-list gio_plate"]/a/@href').extract()[1:2]
        for sub_area in sub_area_list:
            sub_area_url = response.urljoin(sub_area)
            print "sub_area_url: " + sub_area_url
            yield scrapy.Request(sub_area_url, callback=self.get_each_house)

    def get_each_house(self, response):
        house_list = response.xpath('//ul[@class="clinch-list"]/li/div[2]/h2/a/@href').extract()
        for house in house_list:
            housed_detail_url = response.urljoin(house)
            print "housed_detail_url: " + housed_detail_url
            yield scrapy.Request(housed_detail_url, callback=self.get_house_detail)
        next_page_list = response.xpath("//div[@class='page-box house-lst-page-box']/a")
        if next_page_list:
            next_page = next_page_list[-1]
        else:
            return
        if next_page.xpath("@gahref") == 'results_next_page':
            next_page_full_url = response.urljoin(next_page.xpath("@href").extract_first())
            print 'next_page_full_url: ' + next_page_full_url
            yield scrapy.Request(next_page_full_url,
                                 callback=self.get_each_house)
        else:
            return

    def get_house_detail(self, response):
        # print "if i am here:\n"
        # 简单的去重复
        if response.url not in self.all_url:
            self.all_url.add(response.url)
        else:
            return
        # http://sh.lianjia.com/chengjiao/sh1036177.html
        all_data_div = response.xpath("//div[@class='content']")
        item = ShLianjiaChengjiaoItem()

        item['decorate_status'] = all_data_div.xpath("table/tr[3]/td[1]/text()").re_first("\w+")
        item['total_floor'] = all_data_div.xpath("table/tr[2]/td[1]/text()").re_first("\w+/\w+")
        item['house_orientation'] = all_data_div.xpath("table/tr[3]/td[2]/text()").re_first("\w+")
        item['total_price'] = all_data_div.xpath("div[1]/div[2]").re_first("\d+")
        item['floor'] = all_data_div.xpath("table/tr[2]/td[1]/text()").re_first("\w+/\w+")
        item['unit_price'] = all_data_div.xpath("table/tr[1]/td[1]/text()").re_first('\d+')
        item['house_year'] = all_data_div.xpath("table/tr[2]/td[2]/text()").re_first('\w+')

        item['house_structure'] = response.xpath("//div[@class='title-wrapper']/div[1]/h1/text()").extract_first()
        item['name'] = response.xpath("//div[@class='title-wrapper']/div[1]/h1/text()").extract_first()
        item['idx'] = response.xpath("//div[@class='title-wrapper']/div[1]/h1/text()").extract_first()
        item['area'] = response.xpath("//div[@class='title-wrapper']/div[1]/h1/text()").extract_first()
        item['house_structure'] = response.xpath("//div[@class='title-wrapper']/div[1]/h1/text()").extract_first()
        item['xiaoqu_id'] = all_data_div.xpath("table/tr[4]/td/a/text()").extract_first()
        item['deal_time'] = all_data_div.xpath("div[1]/div[1]/p/text()").extract_first()

        item['url'] = response.url
        item['datatype'] = "chengjiao_detail"
        item['province'] = "上海"
        item['site'] = "lianjia"
        item['house_type'] = "na"
        item['city'] = "上海"
        item['pub_time'] = "na"
        item['deal_status'] = "0"
        yield item
