import requests
import csv
import json
from lxml import html

site_vultr = 'https://www.vultr.com/products/cloud-compute/#pricing'
site_digital_ocean = 'https://www.digitalocean.com/pricing/#droplet'

def main():
    data_vultr = get_data_page_vultr(get_page_content(site_vultr))
    print_result(data_vultr)

    save_csv(data_vultr)



def get_page_content(url):
    response = requests.get(url)
    page_content = html.fromstring(response.content)

    return page_content


def get_data_page_vultr(page_content):    
    headers = page_content.xpath('//div[@class="pt__header"]/div[contains(@class, "pt__cell") and not(contains(text(), "Geekbench Score"))]/text()')
    rows = page_content.xpath('//div[@class="pt__body js-body"]//div[@class="pt__row-content"]/div[contains(@class, "pt__cell")]//strong/text()')

    formated_data = (headers, rows)

    return formated_data


def get_data_page_digital(page_content):
    # busca os headers na página 1, pois, esta sessão não apresenta headers detalhados
    headers = get_data_page_vultr()[0]
    rows = page_content.xpath('//')

    formated_data = (headers, rows)

    return formated_data


def save_csv(data):
    with open('csv_file.csv','w') as csv_file:
        for x in data[0]:
            csv_file.write(x + ',')
        for x in range(len(data[1])):
            if x % 5 == 0:
                csv_file.write('\n')
            csv_file.write(data[1][x] + ',')


# def save_json():



def print_result(data):
    print(data[0])
    for x in range(len(data[1])):
        if x % 5 == 0:
            print('\n')
        print(data[1][x], end=', ')



if __name__ == "__main__":
    main()