#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy

class thewhisky(scrapy.Spider):
    name = 'the_whisky'
    allowed_domains = ['www.thewhiskyexchange.com']
    start_urls = ['https://www.thewhiskyexchange.com/c/305/rest-of-the-world-whisky?pg=1']
    custom_settings = {
       'FEED_URI' : 'tmp/the_whisky.csv'
   }
    
    def parse(self,response):
        for i in range(1,14):
            products = response.xpath("//li[@class='product-grid__item']")
            for product in products:
                link = product.css('a.product-card').attrib['href']
                url = response.urljoin(link)
                yield scrapy.Request(url = url, callback= self.parse_details)
         #pagination   
            next_page = f'https://www.thewhiskyexchange.com/c/305/rest-of-the-world-whisky?pg={i}'
            yield scrapy.Request(url = next_page, callback=self.parse)
            
    def parse_details(self,response):
        name = response.css('h1.product-main__name::text').extract_first().strip()
        price = response.css('p.product-action__price::text').extract_first().strip()
        unit_price = response.css('p.product-action__unit-price::text').extract_first().strip()
        desc = response.css('div.product-main__description p::text').extract_first().strip()
        image = response.css('img.product-main__image').attrib['src']
        yield {
            'Name':name,
            'Price':price,
            'Unit price':unit_price,
            'Description':desc,
            'Image':image
        }

