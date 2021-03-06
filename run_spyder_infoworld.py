from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_scraper.spiders.infoworld import InfoworldSpider
from news_scraper.spiders.devmozilla import MozillaDev

process = CrawlerProcess(get_project_settings())
process.crawl(InfoworldSpider)
process.start()