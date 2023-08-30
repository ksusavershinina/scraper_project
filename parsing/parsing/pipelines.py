# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class ItemPipeline:
    def process_item(self, item, spider):
        if item['number_of_buyers'] is not None:
            item['number_of_buyers'] = re.sub(r'\D', '', item['number_of_buyers'])

        if item['book24_score'] is not None:
            item['book24_score'] = re.sub(r'\s', '', item['book24_score'])
            item['book24_score'] = re.sub(r',', '.', item['book24_score'])

        if item['book24_feedback'] is not None:
            item['book24_feedback'] = re.sub(r'[()\s]', '', item['book24_feedback'])

        if item['description'] is not None:
            description = item['description']
            item['description'] = ' '.join(description)
            item['description'] = re.sub(r'\r', '', item['description'])

        return item
