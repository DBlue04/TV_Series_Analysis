import scrapy

class BlogSpider(scrapy.Spider):#crawl multiple web pages
    name = 'narutospider'
    start_url = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        # for title in response.css():
            
        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page,self.parse)

