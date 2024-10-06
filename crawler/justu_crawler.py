import scrapy

#Spider class name
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    #Name of the spider
    name = 'narutospider'

    #The URLs to be scraped from the domain 
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    # #Extracting data from the web
    def parse(self, response):
        #we can use response.css('div.smw-columnlist-container').css('a::attr(href)').extract()
        #to convert the object selector into a list of plain strings
        #or we can use get() for each object select.
        for href in response.css('div.smw-columnlist-container').css('a::attr(href)'):


            extracted_data = scrapy.Request( "https://naruto.fandom.com"+href.get(),
                                      callback=self.parse_jutsu#when Scrapy successfully downloads 
                                      #a page from one of those URLs, it will automatically call 
                                      # parse_jutsu and pass the downloaded content to it.
                                    )
            yield extracted_data

        for href in response.css('a.mw-nextlink'):#-> css of a.mw-nextlink will give us the link in href
            yield response.follow(href, self.parse)
    
    def parse_jutsu(self, response):
        jutsu_name = response.css('span.mw-page-title-main::text').extract()[0]
        jutsu_name = jutsu_name.strip()

        div_selector = response.css('div.mw-parser-output')[0]
        div_html = div_selector.extract()

        soup = BeautifulSoup(div_html).find('div')

        # if soup.find('div',{'id':'quiz_module_desktop_placement_styles'}):
        #     soup.find('div',{'id':'quiz_module_desktop_placement_styles'}).decompose()
        
        # if soup.find('h2',{'id':'quiz_module_destkop_header_styles'}):
        #     soup.find('h2',{'id':'quiz_module_destkop_header_styles'}).decompose()
        
        # if soup.find('a',{'id':'quiz_module_desktop_link_styles'}):
        #     soup.find('a',{'id':'quiz_module_desktop_link_styles'}).decompose()

        jutsu_type=""
        if soup.find('aside'):
            aside = soup.find('aside')
            for cell in aside.find_all('div',{'class':'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name=='Classification':
                        jutsu_type = cell.find('div').text.strip()

            soup.find('aside').decompose()

        jutsu_description = soup.text.strip()
        jutsu_description = jutsu_description.split('Trivia')[0].strip()


        yield dict(   
                    jutsu_name= jutsu_name,
                    jutsu_type = jutsu_type,
                    jutsu_description=jutsu_description
                )
#run: scrapy runspider crawler/justu_crawler.py -o data/jutsus.jsonl
