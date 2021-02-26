import requests
import csv
import json
from lxml import html

site_vultr = 'https://www.vultr.com/products/cloud-compute/#pricing'
site_digital_ocean = 'https://www.digitalocean.com/pricing/#droplet'

def main():
    # data_vultr = get_data_page_vultr(get_page_content(site_vultr))
    # print_result(data_vultr)
    # save_csv(data_vultr)

    data_digital = get_data_page_digital(get_page_content(site_digital_ocean))
    # print(data_digital)
    # save_csv(data_digital)
    save_json(data_digital)



def get_page_content(url):
    response = requests.get(url)
    page_content = html.fromstring(response.content)

    return page_content


def get_data_page_vultr(page_content):    
    headers = page_content.xpath('//div[@class="pt__header"]/div[contains(@class, "pt__cell") and not(contains(text(), "Geekbench Score"))]/text()')
    rows_elements = page_content.xpath('//div[@class="pt__body js-body"]//div[@class="pt__row-content"]/div[contains(@class, "pt__cell")]//strong/text()')

    formated_data = (headers, rows_elements)

    return formated_data


def get_data_page_digital(page_content):
    rows_elements = []
    formated_prices = []

    headers = get_data_page_vultr(get_page_content(site_vultr))[0]              # busca os headers na página 1, pois, esta sessão não apresenta nomes de colunas detalhadamente
    prices = page_content.xpath('//div[@class="topBox"][1]/div//text()[1]')     # retorna lista com '$' e valores, separados, devido ao arranjo dos elementos no html
    for x in range(len(prices)):
        if x == len(prices)-1: break
        if x % 2 == 1: continue
        formated_prices.append(prices[x] + prices[x+1])                         # loop para juntar os '$' com seus respectivos valores
    
    CPUs = page_content.xpath('//div[@class="topBox"]/following-sibling::div//li/span[contains(text(),"/")]/text()[2]') # busca somente a coluna de CPUs disponíveis
    memory = page_content.xpath('//div[@class="topBox"]/following-sibling::div//li[1]/text()[1]')                       # busca somente a coluna de memories disponíveis          
    SSDs = page_content.xpath('//div[@class="topBox"]/following-sibling::div//li[2]/text()[1]')                         # busca somente a coluna de SSDs disponíveis
    transfer = page_content.xpath('//div[@class="topBox"]/following-sibling::div//li[3]/text()[1]')                     # busca somente a coluna de transfers disponíveis
                       
    for x in range(len(CPUs)):                                                  # loop para concatenar todos os valores, respectivamente, em um só array
        rows_elements.append(SSDs[x])
        rows_elements.append(CPUs[x])
        rows_elements.append(memory[x])
        rows_elements.append(transfer[x])
        rows_elements.append(formated_prices[x])

    formated_data = (headers, rows_elements)

    return formated_data


def save_csv(data):
    with open('csv_file.csv','w') as csv_file:
        for x in data[0]:
            csv_file.write(x + ',')
        for x in range(len(data[1])):
            if x % 5 == 0:
                csv_file.write('\n')
            csv_file.write(data[1][x] + ',')


def save_json(data):
    data_dict = {}
    individual_rows = []
    aux = []

    for x in range(len(data[1])):
        if x % 5 == 0 and x != 0:
            individual_rows.insert(len(individual_rows), aux)
            del aux
            aux = []
        aux.append(data[1][x])
        if x == len(data[1])-1:
            individual_rows.insert(len(individual_rows), aux)
            del aux

    for x in range(len(individual_rows)):
        new_row = 'Row'+str(x+1)
        data_dict[new_row] = {}
        for element in range(len(data[0])):
            data_dict[new_row][data[0][element]] = individual_rows[x][element]

    with open('json_file.json','w') as json_file:
        json.dump(data_dict,json_file, ensure_ascii=False, indent=4)


def print_result(data):
    print(data[0])
    for x in range(len(data[1])):
        if x % 5 == 0:
            print('\n')
        print(data[1][x], end=', ')


if __name__ == "__main__":
    main()