#import necessary libraries
import posixpath
import time

#import necessary classes & modules
from urllib.parse import urlparse
from termcolor import colored
from scrapy import spiders
from scrapy import linkextractors

#import sitemap tag fields from items.py
from sitemap_generator import items

#initialise the sitemap class' spider 
class SiteMapSpider (spiders.CrawlSpider):

    #see https://docs.scrapy.org/en/latest/topics/spiders.html for Documentation
    #
    #name of the bot
    name = 'sitemap_generator'

    #the rules that the crawler follows as it crawls through the given website
    #
    #see documentation at https://docs.scrapy.org/en/latest/topics/spiders.html under 'CrawlSpider example'
    rules = [
        spiders.Rule
        (
            linkextractors.LinkExtractor
            (

                #using regular expressions to tell the crawler which urls
                #it must extract
                allow=
                [
                    r'.*\.html',
                    r'.*\.pdf',
                    r'.*\.xml',
                    r'.*\.txt',
                    r'.*/',
                ]
            ),

            #keep the 'follow' value as true so that the spider follows the links
            #and calls back the parse_item function after each link
            follow=True, callback='item_parser'
        )
    ]


    #init by getting the domain, add it to the allowed domains list and
    #the start_urls list, and append any new url to the list
    #
    #see documentation at https://docs.scrapy.org/en/latest/topics/spiders.html under 'Spider arguments'
    def __init__(self, domain, urls='', *args, **kwargs):

        #using super so to avoid repeating the SiteMapSpider class code
        super(SiteMapSpider, self).__init__(*args, **kwargs)

        start_time = time.time()

        #check if the domain name has been inputted correctly and giving
        # a confirmation message, or providing a meaningful error message otherwise
        if domain.startswith("http://"):

            correct_domain = domain[7:]
            print(colored(
                '\nDOMAIN ERROR:\nPlease make sure the domain EXISTS, and IS VALID i.e. does NOT have the "http://" prefix. Stopping\n', 'red'))
            print(colored ('The correct input for the domain you have provided (assuming it exists) should be ', 'blue'), colored('%s \n ' % correct_domain, 'green'))

        elif domain.startswith("https://"):
    
            correct_domain = domain[8:]
            print(colored(
                '\nDOMAIN ERROR:\n Please make sure the domain EXISTS, and IS VALID i.e. does NOT have the "http://" prefix. Stopping\n', 'red'))
            print(colored('The correct input for the domain you have provided (assuming it exists) should be ', 'blue'), colored('%s \n ' % correct_domain, 'green'))

        else:

            #add the domain to the allowed domains list and
            #the start_urls list
            #
            #see documentation at https://docs.scrapy.org/en/latest/topics/spiders.html under 'CrawlSpider example'
            self.domain = domain
            self.allowed_domains = [domain]
            self.start_urls = ['http://%s' % domain]
            print(colored(
                '\nDomain name accepted. Crawling... (this may take several minutes, kindly be patient)\n', 'green'))
        
            #append any new url to the list and ignore any non-URLs
            for url in urls.split(','):
                if not url:
                    continue
                self.start_urls.append(url)


    #the callback function that gets the necessary data from the response
    #as per the sitemap.org Sitemap Protocol
    #
    #see documentation at https://docs.scrapy.org/en/latest/topics/spiders.html under 'XMLFeedSpider example'
    def item_parser(self, response):

        #create a SiteMapFields instance and assign a URL value to the <loc> tag
        #from the response
        item = items.SiteMapFields()
        item['loc'] = response.url

        #use urlparse().path to obtain the path of a webpage
        #and posixpath.basename() to get the filename of a webpage
        path = urlparse(response.url).path
        filename = posixpath.basename(path)


        #check if the headers provide a date for last modification
        if 'Last-Modified' in response.headers:

            #assign a value to the <lastmod> tag from the response headers
            #as a time object
            lastmod = time.strptime(response.headers['Last-Modified'].decode('ascii'),
                                    "%a, %d %b %Y %H:%M:%S %Z")

        else:

            #assign the value for the <lastmod> field as the current date
            lastmod = time.strptime(response.headers['Date'].decode('ascii'),
                                    "%a, %d %b %Y %H:%M:%S %Z")


        #add the <lastmod> value to the item list
        item['lastmod'] = time.strftime("%Y-%m-%d", lastmod)


        #assign default/average values to the <changefreq> and
        #<priority> tags
        item['changefreq'] = 'daily'
        item['priority'] = '0.5'


        #assign a high priority to index HTML pages
        if filename == 'index.html' or filename == '' or filename == 'home.html':
            item['priority'] = '1.0'

        #return the entire item instance
        return item
