# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import necessary libraries
import os
import lxml
import scrapy

#import necessary classes & modules
from scrapy import exporters
from termcolor import colored

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


#sitemap.org <urlset> schema
schema = {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"}


#class to export the URLs to a xml file format by editing the XMLItemExporter
#class to use sitemap.org Sitemap Protocols
class ExporterPipeline(exporters.XmlItemExporter):

    #function to export urls with adjusted attributes to accomodate sitemap.org Sitemap Protocols
    #
    #see documentation at https://docs.scrapy.org/en/latest/_modules/scrapy/exporters.html#BaseItemExporter.export_item 
    #under 'class XmlItemExporter'
    def start_exporting(self):

        try:

            #Set sitemap.org schema attributes
            self.xg.startDocument()
            self.xg.startElement(self.root_element, schema)
            self._beautify_newline(new_item=True)

        except:

            #inform the user if the exporter can't start
            print(colored('\nEXPORTING ERROR:\nFailed to start exporting. Stopping', 'red'))



#class to ignore duplicated URLs.
#
#see documentation  at https://docs.scrapy.org/en/latest/topics/item-pipeline.html under 'Duplicates Filter'
class DuplicatesPipeline(object):

    #init a set() instance to parse through
    def __init__(self):
        self.urls_crawled = set()


    #process the URL items for export for the DuplicatesPipeline class
    def process_item(self, item, spider):

        try:
            
            #call an item adapter instance
            url = ItemAdapter(item)
            #Check if a URL already exists
            if url['loc'] in self.urls_crawled:

                #raise exception for found duplicate
                raise scrapy.exceptions.DropItem("Duplicate URL found: %s."
                                                % item['loc'])

            else:

                #add the URL to the item list
                self.urls_crawled.add(url['loc'])
                return item

        except AttributeError:

            #inform the user if the items cant be processed
            print(colored('\nPROCESSING ERROR:\nFailed to process URL items. Stopping', 'red'))



#class to export the URLs to a sitemap.xml file
class SitemapExporterPipeline:
    
    #init variable for files and the exporter
    def __init__(self):
        self.files = {}
        self.exporter = None


    #create a pileline instance
    #
    #see documentation at https://docs.scrapy.org/en/latest/topics/signals.html#topics-signals
    @classmethod
    def from_crawler(cls, crawler):
        try:

            sitemap_exporter_pipeline = cls()

            #connect the signals from the opened spider to the exporter pipeline and 
            #the scrapy signals method
            crawler.signals.connect(sitemap_exporter_pipeline.spider_opened,
                                    scrapy.signals.spider_opened)


            #connect the signals from the closed spider to the exporter pipeline and
            #the scrapy signals method
            crawler.signals.connect(sitemap_exporter_pipeline.spider_closed,
                                    scrapy.signals.spider_closed)

            #return the class method
            return sitemap_exporter_pipeline

        except AttributeError:

            #inform the user if the crawler can't make the connections
            print(colored('\nSIGNAL ERROR:\nFailed to connect crawler signals. Stopping', 'red'))


    #method for the spider to start crawling
    #
    #see documentation at https://docs.scrapy.org/en/latest/topics/exporters.html under 'Using Item Exporters'
    def spider_opened(self, spider):

        try:
            
            #variable to create a sitemap.xml file and define the <urlset> tags only
            output = open(os.path.join(os.getcwd(), '%s_sitemap.xml' % spider.domain), 'w+b')


            #check if the file was successfuly created
            if os.path.exists("%s_sitemap.xml" % spider.domain):

                #inform the user that the file was created successfully
                print(colored('\nThe file "%s_sitemap.xml" has been successfully created. Attempting to export URLs to the file\n' % spider.domain, 'green'))

            else:

                #inform the user that the file could not be created
                print(colored(
                    '\nFILE ERROR:\nFailed to create "%s_sitemap.xml" file. Stopping\n' % spider.domain, 'red'))


            #start exporting the output from the spider to the file
            self.files[spider] = output
            self.exporter = ExporterPipeline(output, item_element='url',
                                                root_element='urlset')
            self.exporter.start_exporting()

        except AttributeError:

            #inform the user that there was problem crawling or exporting the data
            print(colored('\nCRAWL ERROR:\nSpider encountered error when starting crawl/exporting to XML file.\nPlease check that the domain EXISTS, and IS VALID i.e. does NOT have the "http://" or "https://" prefixes. Stopping\n', 'red'))



    #method for the spider to stop crawling
    #
    #see documentation at https://docs.scrapy.org/en/latest/_modules/scrapy/exporters.html#BaseItemExporter.export_item 
    #under 'class XmlItemExporter'
    #and at https://docs.scrapy.org/en/latest/topics/exporters.html under 'Using Item Exporters'
    def spider_closed(self, spider):

        try:

            #finish exporting the data, pop it to the files variable
            #and close the file 
            self.exporter.finish_exporting()
            output = self.files.pop(spider)
            output.close()


            #variable to parse the data 
            xml_tree = lxml.etree.parse(os.path.join(
                os.getcwd(), "%s_sitemap.xml" % spider.domain))


            #open the file and convert the data to string format, and then 
            #structure it into pretty printed xml trees 
            with open(os.path.join(os.getcwd(), "%s_sitemap.xml" % spider.domain),
                    'w+b') as field_tags:
                field_tags.write(lxml.etree.tostring(xml_tree, pretty_print=True))


            #check if the file exists and was written to successfully and inform the user of the same
            if os.path.exists("%s_sitemap.xml" % spider.domain) and os.path.getsize("%s_sitemap.xml" % spider.domain) > 70:

                print(colored(
                    '\nSUCCESS!\nSitemap created successfully and exported to "%s_sitemap.xml" file.\n' % spider.domain, 'green'))
    
            else:

                #inform the user that there was problem writing the data onto the file
                print(colored(
                    '\nFILE ERROR:\nError writing URL data to "%s_sitemap.xml" file. The domain you have given, or alternatively the file, may not exist. Stopping\n' % spider.domain, 'red'))

        except AttributeError:

            #inform the user that there was problem crawling or exporting the data
            print(colored('\nCRAWL ERROR:\nSpider encountered error when finishing crawl/exporting to XML file.\nPlease check that the domain EXISTS, and IS VALID i.e. does NOT have the "http://" or "https://" prefixes. Stopping\n', 'red'))


    #process the URL items for export for the SiteMapExporterPipeline class
    #
    #see documentation at https://docs.scrapy.org/en/latest/_modules/scrapy/exporters.html#BaseItemExporter.export_item 
    #under 'class XmlItemExporter' 
    #and at https://docs.scrapy.org/en/latest/topics/exporters.html under 'Using Item Exporters'
    def process_item(self, item, spider):

        try:

            #export the items
            self.exporter.export_item(item)
            return item

        except AttributeError:

            #inform the user that there was an error processing the item
            print(colored('\nPROCESSING ERROR:\nFailed to process the items for export. Stopping', 'red'))