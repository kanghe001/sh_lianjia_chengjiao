# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ShLianjiaChengjiaoPipeline(object):
    def process_item(self, item, spider):
        print "I am in pipelines"
        item_dict = dict(item)
        tar_get_file = codecs.open("./hz_lianjia_chengjiao_20161021.json", 'a', encoding='utf-8')
        item_json = json.dumps(item_dict, ensure_ascii=False)
        tar_get_file.write(item_json + '\r\n')
        return item
