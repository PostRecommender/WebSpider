#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from WebSpider.items import JobItem
from scrapy import Request


def parse_job(response):
    try:
        item = JobItem()
        item['job_name'] = response.xpath(
            '//div[@class="inner-left fl"]/h1/text()'
        ).extract()[0]
        item['job_exp'] = response.xpath(
            '//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()'
        ).extract()[0]
        test = response.xpath(
            '//p[@class="company-name-t"]/a/text()'
        ).extract()[0]
        item['company_name'] = test

        item['company_welfare'] = response.xpath(
            '//div[@class="welfare-tab-box"]/span/text()'
        ).extract()
        item['job_pay'] = response.xpath(
            '//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()'
        ).re('(\d+-*\d+元)')[0]
        item['job_workplace'] = response.xpath(
            '//ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()'
        ).extract()[0]
        item['job_min_edu'] = response.xpath(
            '//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()'
        ).extract()[0]
        desc = response.xpath('//div[@class="tab-inner-cont"][1]/p/text()').extract()
        item['job_dec'] = desc
        # todo: 公司介绍没法完全匹配
        item['company_size'] = response.xpath(
            '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()'
        ).extract()[0]
        item['company_ind'] = response.xpath(
            '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[3]/strong/a/text()'
        ).extract()[0]

        yield item
    except IndexError as error:
        print(error)


class JobSpider(scrapy.Spider):
    name = 'zlzp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    allowed_domains = ["sou.zhaopin.com", "jobs.zhaopin.com"]

    def start_requests(self):
        keys = ['大数据', 'hadoop', 'spark']
        for key in keys:
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=选择地区&kw=' + key + '&sm=0&p=1'
            yield Request(url=url, headers=self.headers)

    def parse(self, response):
        links = response.xpath('//td[@class="zwmc"]/div/a[1]/@href').extract()
        for link in links:
            yield Request(link, callback=parse_job, headers=self.headers, )

        next_url = response.xpath('//a[@class="next-page"]/@href').extract()
        if next_url:
            yield Request(next_url[0])
