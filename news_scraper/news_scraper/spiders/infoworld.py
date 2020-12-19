import scrapy


class InfoworldSpider(scrapy.Spider):
    name = 'infoworld'
    allowed_domains = ['infoworld.com']
    start_urls = [
            'https://www.infoworld.com/category/machine-learning/',
            'https://www.infoworld.com/category/cloud-computing/'
            ]
    custom_settings = {
            'DEPTH_LIMIT': 5,
            'FEED_FORMAT': 'json',
            'FEED_URI': 'infoworld_news.json',
            'FEED_EXPORT_ENCODING': 'utf-8'
            }

    def parse(self, response):
        promo_articles_urls = response.xpath('//section[@class="bodee"]/div[@class="main-col"]/div[contains(@class, "index-promo")]/div[@class="promo-headline"]//a/@href').getall()
        if promo_articles_urls:
            for promo_article_url in promo_articles_urls:
                yield response.follow(promo_article_url, callback=self.parse_article)

        articles_urls = response.xpath('//section[@class="bodee"]/div[@class="main-col"]//div[@class="post-cont"]/h3/a/@href').getall()
        if articles_urls:
            for article_url in articles_urls:
                yield response.follow(article_url, callback=self.parse_article)

        next_articles = response.xpath('//section[@class="bodee"]/div[@class="main-col"]/a[@id="load-more-index"]/@href').get()
        if next_articles:
            yield response.follow(next_articles, callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//section[@role="main"]//h1[@itemprop="headline"]/text()').get()
        if not title:
            yield
        overview = response.xpath('//section[@role="main"]//h3[@itemprop="description"]/text()').get()
        url = response.url
        image_url = response.xpath('//section[@role="main"]//div[@class="lede-container"]/figure/img/@data-original').get()
        body = response.xpath('//section[@class="bodee"]/div[@class="cat "]//*[self::p or self::h2 or self::a or self::li]/text()').getall()
        body = ''.join(body)
        pub_date = response.xpath('//head/meta[@name="date"]/@content').get()
        yield {
                'title': title,
                'overview': overview,
                'url': url,
                'body': body,
                'pub_date': pub_date
                }
