# -*- coding: utf-8 -*-
import scrapy


class TrilhasSpider(scrapy.Spider):
    name = "trilhas"
    allowed_domains = ["thedevelopersconference.com.br"]
    start_urls = [
        'http://www.thedevelopersconference.com.br/tdc/2016/florianopolis/trilhas',
    ]
    download_delay = 1.0

    def parse(self, response):
        trilhas_urls = response.xpath(
            '//div[@id="trilhas-florianopolis"]'
            '/div[@class="row"][1]//a[contains(@href, "trilha-")]/@href'
        ).extract()
        for trilha_url in trilhas_urls:
            yield scrapy.Request(response.urljoin(trilha_url), callback=self.parse_trilha)

    def parse_trilha(self, response):
        for author in response.xpath('//a[starts-with(@href, "#minibio")]'):
            yield {
                'trilha': response.css('h1.titulo-trilha ::text').re_first('Trilha (.*)'),
                'palestra': author.xpath('normalize-space(./text())').extract_first(),
                'palestrante': author.xpath(
                    'normalize-space(./preceding-sibling::a[starts-with(@href, "#descricao-")][1]/text())'
                ).extract_first()
            }
