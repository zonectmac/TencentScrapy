import scrapy
from TencentCast.items import TencentcastItem


class TencentSpider(scrapy.Spider):
    name = 'tencentcast'
    # allowed_domains = 'hr.tencent.com'
    base_url = 'https://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
            item = TencentcastItem()
            item['positionName'] = str(node.xpath("./td[1]/a/text()").extract()[0].encode('utf-8'))
            item['positionLink'] = str(node.xpath("./td[1]/a/@href").extract()[0].encode('utf-8'))
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = str(node.xpath("./td[2]/text()").extract()[0].encode('utf-8'))
            else:
                item['positionType'] = ""
            item['peopleNumber'] = str(node.xpath("./td[3]/text()").extract()[0].encode('utf-8'))
            item['workLocation'] = str(node.xpath("./td[4]/text()").extract()[0].encode('utf-8'))
            item['publishTime'] = str(node.xpath("./td[5]/text()").extract()[0].encode('utf-8'))

            yield item
        # if self.offset < 100:
        #     self.offset += 10
        #     url = self.base_url + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)
        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            nexturl = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com" + nexturl, callback=self.parse)
