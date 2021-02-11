# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from datetime import datetime


class CareerCsvWriterPipeline:

    def open_spider(self,spider):
        f = open(f'{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv','w',newline="")
        fieldnames = [
            'job_title',
            'fee',
            'nearest_station',
            'contract',
            'language',
            'skill',
            'job_content'
        ]

        self.f = f
        self.writer = csv.DictWriter(f,fieldnames=fieldnames)
        self.writer.writeheader()
    
    def close_spider(self,spider):
        self.f.close()


    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
