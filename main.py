import requests
import csv
import json
from lxml import html

site_vultr = 'https://www.vultr.com/products/cloud-compute/#pricing'
site_digital_ocean = 'https://www.digitalocean.com/pricing/#droplet'

def main():
    get_table_page1(get_page_content(site_vultr))



def get_page_content(url):
    response = requests.get(url)
    page_content = html.fromstring(response.content)

    return page_content


def get_table_page1(page_content):
    headers = page_content.xpath('//div[@class="pt__header"]/div[contains(@class, "pt__cell") and not(contains(text(), "Geekbench Score"))]/text()')

    rows = page_content.xpath('//div[@class="pt__body js-body"]//div[@class="pt__row-content"]/div[contains(@class, "pt__cell")]//strong/text()')

    print(headers)
    print(rows)




def get_table_page2(page_content):
    headers = page_content.xpath()

    rows = page_content.xpath()



def save_csv():



def save_json():



if __name__ == "__main__":
    main()