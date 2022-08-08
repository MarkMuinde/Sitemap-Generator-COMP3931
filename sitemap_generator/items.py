# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


#import necessary library
import scrapy


#initialise the sitemap class for each field in a sitemap <url> parent tag
#as per sitemap.org Sitemap Protocol documentation

class SiteMapFields(scrapy.Item):
    
    # define the fields for your item here:
    #
    #see https://sitemaps.org/protocol.html for documentation
    loc = scrapy.Field()
    lastmod = scrapy.Field()
    changefreq = scrapy.Field()
    priority = scrapy.Field()
