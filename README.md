# COMP3931
Individual Project 2021/22

## Name
Sitemap Generator

## Description
This project is a sitemap generator using the <a href=https://docs.scrapy.org/en/latest/index.html#>Scrapy Framework</a>, it uses a command line interface that takes the domain name of a public website from the user and returns a XML sitemap of the website.

## Installation
The repository comes with its own virtual environment labelled 'flask', so all you have to do is clone this repository into your computer.

## Usage
1. Clone the project onto your computer. It is a public repository so there is open access to it.

2. cd into the root directory of the project.

3. Once you are in the root repository, activate the virtual environment by running the following command: 

                            source flask/bin/activate

4. Once the virtual environment is running, use the sitemap generator by running the following command:

                            scrapy crawl sitemap_generator -a domain=<domain_name>

    where <domain_name> is the user input, the domain name of a public website.

    For example, if you want to get the sitemap of the website 'http://website.com', the command will be:

                            scrapy crawl sitemap_generator -a domain=website.com

5. Once you have run this command, the generator will crawl the website and return a XML sitemap file in the root directory of the project.<br>The program may take several minutes depending on the size of the website, so kindly be patient.

6. Once complete, the program will inform you that the sitemap has been generated and give you the filename of the same

## Support
If you want to learn further about sitemaps or Scrapy, kindly visit https://sitemaps.org and https://docs.scrapy.org/en/latest/index.html respectively.

## Authors 
Mark Muinde

(The code has been partly adapted from Scrapy Framework documentation. Specifics are available at the relevant functions.)


## Project status
Completed
