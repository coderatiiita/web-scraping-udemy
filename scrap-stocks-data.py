#!/usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import sys
import pprint

def main():    
    url = 'https://finance.yahoo.com/quote/'
    q_param = ''
    if len(sys.argv) == 2:
        q_param = sys.argv[1]
    else:
        q_param = 'AAPL'
    str = '?p='
    complete_url = url + q_param + str + q_param
    print(complete_url)

    resp = requests.get(complete_url)
    if resp.status_code != 200:
        print('yahoo finance server sent bad response. http status code {}'.format(resp.status_code))
        exit(1)

    soup = BeautifulSoup(resp.text, features='html.parser')


    contents_div = soup.find('div', {'id' : 'quote-summary'})
    #tables = contents_div.find_all('tables')
    trs = contents_div.find_all('tr')

    def get_stock_values(table_rows):
        stock_values = {}
        for idx, row in enumerate(table_rows):
            tds = row.find_all('td')
            stock_values[tds[0].text] = tds[1].text
            #print(idx, tds[0].text, tds[1].text)
        #print('--------------------------------------------------------------------------------')
        return stock_values

    stock_vals = get_stock_values(trs)
    pp = pprint.PrettyPrinter(indent=6, depth=6)
    pp.pprint(stock_vals)

    

if __name__ == '__main__':
    main()




