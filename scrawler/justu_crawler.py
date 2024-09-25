import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):#crawl multiple web pages
    name = 'narutospider'
    start_url = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        for href in response.css('.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extracted_data = scrapy.Request('https://naruto.fandom.com' + href, callback=self.parse_justu)
            return extracted_data
            
        #after crawling all the content of the current page, we will
        # move to the next 250 page to get the new content    
        for next_page in response.css('a.mw-nextlink'):
            # follow a new URL discovered while processing the current response.
            yield response.follow(next_page,self.parse)

        def parse_justu(self, response):
            jutsu_name = response.css('span.mw-page-title-main::text').extract()[0]
            jutsu_name = jutsu_name.strip()

            div_selector = response.css('div.mw-parser-output')[0]
            div_html = div_selector.extract()

            soup = BeautifulSoup(div_html).find('div')

            if soup.find('aside'):
                aside = soup.find('aside')

                for cell in aside.find_all('div',{'class':'pi-data'}):
                    if cell.find('h3'):
                        cell_name = cell.find('h3').text.strip()
            
            soup.find('aside').decompose()

            jutsu_description = soup.text.strip()
            jutsu_description = jutsu_description.split('Trivia')[0].strip()

            return dict{
                jutsu_name = jutsu_name,
                jutsu_type = jutsu_type,
                jutsu_description = jutsu_description
            }
            
