# -*- coding: utf-8 -*-
import scrapy


class PalestrantesSpider(scrapy.Spider):
    name = "palestrantes"
    allowed_domains = ["thedevelopersconference.com.br"]
    start_urls = [
        'http://www.thedevelopersconference.com.br/tdc/2016/florianopolis/trilhas',
    ]
    #download_delay = 0.5

    def parse(self, response):
        trilhas_urls = response.xpath(
            '//div[@id="trilhas-florianopolis"]'
            '/div[@class="row"][1]//a[contains(@href, "trilha-")]/@href'
        ).extract()
        for trilha_url in trilhas_urls:
            yield scrapy.Request(response.urljoin(trilha_url), callback=self.parse_trilha)

    def parse_trilha(self, response):
        trilha = response.css('h1.titulo-trilha ::text').re_first('Trilha (.*)')
        for palestrante in response.css('div[id^="minibio"]'):
            yield {
                'trilha': trilha,
                'nome': palestrante.css('h4 ::text').re_first('\w.+'),
                'social_links': palestrante.css('.col-xs-12.text-left a ::attr(href)').extract()
            }

