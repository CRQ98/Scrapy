import scrapy
from urllib.parse import urljoin
from myspider.items import ParticipantItem, EventItem # type: ignore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup


class RomicsSpider(scrapy.Spider):
    name = "romics"
    allowed_domains = ["www.romics.it"]
    start_urls = ["https://www.romics.it"]

    def __init__(self, *args, **kwargs):
        super(RomicsSpider, self).__init__(*args, **kwargs)
        # SET options
        options = Options()
        options.add_argument("--headless")  # headless
        self.driver = webdriver.Chrome(options=options)  # no require path

        self.participant_order=0
        self.event_order=0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        yield response.follow("it/speakers-xxxiv-edizione", callback=self.parse_participants)
        yield response.follow("it/programma-all", callback=self.parse_events)

    def parse_time(self,timestr):
        parts = timestr.split()
        if len(parts) < 5:
            return None 
        day = parts[1]
        month_str = parts[2]
        start_time = parts[3]
        end_time = parts[5]
        # get this year
        year = datetime.now().year
        # parse time
        start_dt = datetime.strptime(f"{day} {month_str} {year} {start_time}", "%d %b %Y %H:%M")
        end_dt = datetime.strptime(f"{day} {month_str} {year} {end_time}", "%d %b %Y %H:%M")
        
        return {
        "startDate": start_dt.strftime("%Y-%m-%d"),
        "startHour": start_dt.strftime("%H:%M"),
        "endHour": end_dt.strftime("%H:%M")
        }

    def parse_participants(self,res):
        guests = res.css('ul#blazy-views-guest-test-1-page-page-7-1 h5 a::attr(href)').getall()


        for guest in guests:
            item = ParticipantItem()
            #order
            item['order'] = self.participant_order
            self.participant_order += 1
            
            url=res.urljoin(guest)  
            yield scrapy.Request(url,callback=self.parse_participant, meta={'item': item})

    def parse_participant(self,response):
        item = response.meta['item']

        # load page
        self.driver.get(response.url)
        time.sleep(1)
        body = self.driver.page_source
        res = scrapy.http.HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

        #start parse data
        item['name'] = res.css("h1.page-title::text").get()
        item['profileImageId']= res.urljoin(res.xpath('/html/body/div[2]/div/div[5]/div[2]/div/article/div/div[1]/div/div/div[1]/div/div/div/div/div/img/@src').get())
        item['bio']=self.html_parse(''.join(res.css('.field--name-field-bio-sum p').getall()))
        item['pageType']= "person"


        #check
        print('\n--------------------------------')
        print(item)
        print('\n--------------------------------')

        yield item

    def parse_events(self, res):
        divs = res.css('.view-content > div')
        for div in divs:
            item = EventItem()
            item['name'] = div.css('.col-lg-6 h4::text').get()
            item['extraAddress'] = div.css('div:nth-child(3) h5::text').get().strip()
            info= self.parse_time(div.css('div:nth-child(1) h5::text').get())
            item['startDate'] = info['startDate']
            item['startHour'] = info['startHour']
            item['endHour'] = info['endHour']
            item['ticketsMinPrice'] = "10.0"
            item['freeEntry'] = "false"
            item['pageIds'] = "romics"
            item['status'] = "published"
            item['ownerId'] = "manfredo-di-porcia-56251396"
            item['eventUrl'] = res.url

            #order
            item['order'] = self.event_order
            self.event_order += 1

            bottom = div.css('.col-lg-3 p a::attr(href)').get()
            description=None
            if bottom:
                full_url = res.urljoin(bottom)
                item['eventUrl'] = full_url
                yield scrapy.Request(url=full_url, callback=self.parse_events_detail, meta={'item': item})
            else:
                # not detail direct output
                description=div.css('.col-lg-6 p::text').get()
                #check if description is empty
                if description:
                    item['description'] = re.sub(r'\s+', ' ', description)
                else:
                    item['description'] = ''

                yield item        
            

    def parse_events_detail(self, response):
        # get form meta
        item = response.meta['item']

        # use selenium 
        self.driver.get(response.url)
        time.sleep(1)
        body = self.driver.page_source
        res = scrapy.http.HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

        # fill item
        item['description'] = self.html_parse(''.join(response.css('.field__item .clearfix p').getall()))
        item['coverImageId'] = response.urljoin(res.css('.media img::attr(src)').get()) 
        
        #check
        print('\n--------------------------------')
        print(item)
        print('\n--------------------------------')
        
        yield item

    def html_parse(self,html):
        soup = BeautifulSoup(html, 'lxml')
        [br.replace_with('\n') for br in soup.find_all('br')]
        #[a.decompose() for a in soup.find_all('a')]
        paragraphs = soup.find_all('p')
        text=[p.get_text().strip() for p in paragraphs]
        fulltext="\n\n".join(text)
        #extra clean
        cleaned_text = "\n".join([re.sub(r'\s+', ' ', line).strip() for line in fulltext.splitlines()])
        return cleaned_text

    def closed(self, reason):
        # close
        self.driver.quit()
        print(f'Now : {datetime.now().strftime("%H:%M:%S")}')