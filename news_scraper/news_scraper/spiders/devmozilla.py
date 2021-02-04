import scrapy

#articles_titles = response.xpath('//h3[@class="post__title"]/a/text()').getall()
#Articles_url = response.xpath('//h3[@class="post__title"]/a/@href').getall()
#Articles_overview = response.xpath('//p[@class="post__tease"]/text()').getall()
#next page = response.xpath('//span[@class="nav-paging__next"]/a/@href').get()
#body= response.xpath('//article[@class="post"]/*[self::p or child::a or self::h2]/text()').getall()
#date = response.xpath('//abbr[@class="published"]/text()').get()


class MozillaDev(scrapy.Spider):
    name = 'mozilladev'
    start_urls = [
        
        'https://hacks.mozilla.org/articles/'

    ]
    allowed_domains = ['mozilla.org']
    custom_settings = {
        'FEED_URI':'articles.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 5
    }

    def parse_articles_body(self, response, **kwargs):
        body= response.xpath('//article[@class="post"]//*[self::p or self::a or self::h2 or self::span]/text()').getall()
        body = ''.join(body)
        date = response.xpath('//abbr[@class="published"]/text()').get()
        yield { 'title': kwargs['title'],
                'overview': kwargs['overviews'],
                'url':kwargs['urls'], 
                'body':body,
                'pub_date':date
            } 


    def parse_pages(self, response, **kwargs):
        if kwargs:
            
            # titles = kwargs['Article Titles']
            titles = kwargs['Articles Titles']
            urls =  kwargs['Articles Urls']
            overviews = kwargs['Articles Overview']
            articles_titles = response.xpath('//h3[@class="post__title"]/a/text()').getall()
            articles_url = response.xpath('//h3[@class="post__title"]/a/@href').getall()
            articles_overview = response.xpath('//p[@class="post__tease"]/text()').getall()
            for i  in range(len(urls)):
                yield response.follow(urls[i], callback=self.parse_articles_body, cb_kwargs = {'title':titles[i], 'overviews': overviews[i], 'urls':urls[i]})

            # overviews = kwargs['Articles Overview']

        # titles.append(response.xpath('//h3[@class="post__title"]/a/text()').getall())
        # urls.append(response.xpath('//h3[@class="post__title"]/a/@href').getall())
        # overviews.append(response.xpath('//p[@class="post__tease"]/text()').getall())
       
     
        # yield {
        #         'Articles Titles': articles_titles,
        #         'Articles Urls': articles_url,
        #         'Articles Overview': articles_overview            
        #         }
        next_page_button_link = response.xpath('//span[@class="nav-paging__next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_pages, cb_kwargs = {'Articles Titles':articles_titles, 'Articles Urls':  articles_url, 'Articles Overview': articles_overview})


    def parse(self, response):
       
        articles_titles = response.xpath('//h3[@class="post__title"]/a/text()').getall()
        articles_url = response.xpath('//h3[@class="post__title"]/a/@href').getall()
        articles_overview = response.xpath('//p[@class="post__tease"]/text()').getall()

        # yield {
        #     'Articles Titles': articles_titles,
        #     'Articles Urls': articles_url,
        #     'Articles Overview': articles_overview
            
        # }

        next_page_button_link = response.xpath('//span[@class="nav-paging__next"]/a/@href').get()
        # if next_page_button_link:
        #     yield response.follow(next_page_button_link, callback=self.parse_all_articles, cb_kwargs = {'Article Titles':articles_titles, 'Articles Urls': articles_url, 'Articles Overview': articles_overview})
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_pages, cb_kwargs = {'Articles Titles':articles_titles,'Articles Urls': articles_url, 'Articles Overview': articles_overview})

        
    