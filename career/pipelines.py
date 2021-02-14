# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe
import json
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
import pandas as pd

class CareerSpreadWriterPipeline:
    def open_spider(self,spider):
        '''
        概要
        スパイダー実行時に実行される関数

        処理内容
        スプレッドシートの設定
        データフレームの生成
        '''

        # google dirve API google spreadsheet APIをscopeに記載する
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        #認証情報設定
        #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
        credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-304800-6c876c7ce892.json', scope)

        #OAuth2の資格情報を使用してGoogle APIにログインします。
        gc = gspread.authorize(credentials)

        #共有設定したスプレッドシートキーを変数に設定
        SPREADSHEET_KEY = '11WS_OseE9mJ64SY4wthFVzKhoUovjbdRaF1PREz83nI'

        self.ws = gc.open_by_key(SPREADSHEET_KEY).sheet1

        cols = [
            'job_title',
            'fee',
            'nearest_station',
            'contract',
            'language',
            'skill',
            'job_content'
        ]

        self.df = pd.DataFrame(index=[],columns=cols)
        self.idx = 1


    def process_item(self,item,spider):
        '''
        概要
        yieldするたびに実行するメソッド

        データフレームに値を追加していく

        言語の数の分だけその他のデータも同一内容を追加していく
        '''
        self.df.loc[self.idx] = ItemAdapter(item).asdict()
        self.idx += 1
        print(self.df.tail(5))

    def close_spider(self,spider):
        '''
        概要
        スパイダー終了時に実行されるメソッド

        データフレームをスプレッドシートに書き込む
        '''
        set_with_dataframe(self.ws,self.df.reset_index())




class CareerCsvWriterPipeline:

    def open_spider(self,spider):
        f = open(f'{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv','w',newline="",encoding='Shift-JIS')
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
