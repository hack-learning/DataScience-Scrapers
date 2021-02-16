import base64
import os

# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from news_scraper.spiders.infoworld import InfoworldSpider
# from news_scraper.spiders.devmozilla import MozillaDev



def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(InfoworldSpider)
    # process.crawl(MozillaDev)
    # process.start()

    os.system('python run_spyder_infoworld.py')
    
    return 'ok'