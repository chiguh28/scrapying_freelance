import scrapy
from bs4 import BeautifulSoup
from career.items import CareerItem
import re

class LevtechSpider(scrapy.Spider):
    name = 'levtech'
    allowed_domains = ['freelance.levtech.jp']
    start_urls = ['https://freelance.levtech.jp/project/search/']

    def parse(self, response):
        job_title = ''
        fee = ''
        nearest_station = ''
        contract = ''
        language = []
        skill = ''
        job_content = ''

        soup = BeautifulSoup(response.body,"html.parser")

        # 各項目ごとに取得する
        job_list = soup.find_all("li",class_="prjList__item")


        for job in job_list:

            #案件タイトル取得
            ttl = job.find('h3',class_='prjHead__ttl')
            job_title_block = ttl.find('a')
            if not job_title_block is None:
                job_title = job_title_block.text

            # 料金
            fee_text = job.find('span').text
            if '円' in fee_text:
                fee = int(fee_text.replace('円','').replace(',','')) # 整数型で取得しておきたいため不要な文字を削除する
            
            # 最寄り駅
            nearest_station_block = job.find('li',class_='prjContent__summary__location')
            if not nearest_station_block is None:
                nearest_station = nearest_station_block.text

            # 契約形態
            contract_block = job.find('li',class_='prjContent__summary__contract')
            if not contract_block is None:
                contract = contract_block.text

            # 開発環境 (p.prjTable__item__desc 以下に記載があるため)
            p_item = job.find('p',class_='prjTable__item__desc')
            if p_item:
                link_list = p_item.find_all('a',class_='tagLink')
                for tag_link in link_list:
                    language.append(tag_link.text)
            
            # 求めるスキル
            skill_block = job.find('p',class_='prjTable__item__desc prjTable__item__desc--clamp')
            if not skill_block is None:
                skill = skill_block.text
            
            # 仕事内容
            job_content_block = job.find('p',class_='prjComment__txt__clamp')
            if not job_content_block is None:
                job_content = job_content_block.text

            yield CareerItem(
                job_title = job_title,
                fee = fee,
                nearest_station = nearest_station,
                contract = contract,
                language = language,
                skill = skill,
                job_content = job_content 
            )

        # 再帰的にページを辿る
        next_span_block = soup.find('span',class_='next')
        if next_span_block is None:
            # 次のリンクは無いため終了させる
            return

        next_link = next_span_block.find('a')['href']

        # 相対パスの場合、絶対パスに変換する
        next_link = response.urljoin(next_link)

        print(f'next crowling:{next_link}')
        # 次のページをリクエストする
        yield scrapy.Request(next_link,callback=self.parse)

        
