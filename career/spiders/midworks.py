import scrapy
from bs4 import BeautifulSoup
from career.items import CareerItem


class MidworksSpider(scrapy.Spider):
    name = 'midworks'
    allowed_domains = ['mid-works.com']
    start_urls = ['https://mid-works.com/projects?']

    def parse(self, response):
        job_title = ''
        fee = ''
        nearest_station = ''
        contract = ''
        language = []
        skill = ''
        job_content = ''

        soup = BeautifulSoup(response.body,"html.parser")

        # 案件の項目ブロック毎に取得していく
        job_list = soup.find_all("div",class_="project-list mb-4 shadow-sm")

        for job in job_list:
            # タイトル取得
            # 最初のh2タグが案件タイトルのため、h2タグを取得する
            job_title_box = job.find('h2')
            if job_title_box is not None:
                job_title = job_title_box.text

            # タイトル以外の項目は全てdiv.rowの中に格納されているため、div.rowを全て取得する
            row_list = job.find_all('div',class_='row')

            for row in row_list:
                # 下記で抽出した項目が抽出したい内容のブロックを示しているため、項目ごとに処理を分ける
                item = row.find('div',class_='col-sm-2 font-weight-bold')
                if item is not None:
                    item = item.text
                    if '単価/月' in item:
                        fee_text = row.find('span')
                        if fee_text is not None:
                            # 数値変換したいため不要な文字を削除、変換する
                            fee_text = fee_text.text.replace('~','').replace(' ','').replace('万円','0000')
                            fee = int(fee_text) 
                        
                    elif '勤務地' in item:
                        nearest_station_box = row.find('div',class_='col-sm-10')
                        if nearest_station_box is not None:
                            nearest_station = nearest_station_box.text
                            
                    elif '開発環境' in item:
                        language_box = row.find_all('a')
                        if language_box is not None:
                            for a in language_box:
                                language.append(a.text)
                    

                    elif '業務内容' in item:
                        job_content_box = row.find('div',class_='col-sm-10')
                        if job_content_box is not None:
                            job_content = job_content_box.text
                        
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
        next_page_block = soup.find('a',class_='page-link',rel='next')
        if next_page_block is None:
            # 次のリンクは無いため終了させる
            return

        next_link = next_page_block['href']

        # 相対パスの場合、絶対パスに変換する
        next_link = response.urljoin(next_link)

        print(f'next crowling:{next_link}')
        # 次のページをリクエストする
        yield scrapy.Request(next_link,callback=self.parse)

