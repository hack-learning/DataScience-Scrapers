import scrapy


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['platzi.com']
    start_urls = ['http://platzi.com/datos/']
    custom_settings = {
            'DEPTH_LIMIT': 0,
            'FEED_FORMAT': 'json',
            'FEED_URI': 'courses.json',
            'FEED_EXPORT_ENCODING': 'utf-8'
            }

    def parse(self, response):
        courses_urls = response.xpath('//div[@class="RoutesList"]//div[@class="RoutesList-items"]/a/@href').getall()
        for course_url in courses_urls:
            yield response.follow(course_url, callback=self.parse_course)

    def parse_course(self, response):
        title = response.xpath('//div[@class="Hero"]//div[@class="Hero-info"]//div[@class="Hero-course"]//h1/text()').get()
        badge_url = response.xpath('//div[@class="Hero"]//div[@class="Hero-badge"]/figure/img/@src').get()
        url = response.url
        overview = response.xpath('//div[@class="Hero-course-description"]/span/text()').get()
        yield {
                'title': title,
                'badge_url': badge_url,
                'url': url,
                'overview': overview
                }

