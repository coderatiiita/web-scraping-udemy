#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path

def main():

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    print(url)


    resp = requests.get(url)


    if resp.status_code != 200:
        print('Server sent bad response. HTTP Status Code: {}'.format(resp.status_code))
        exit(1)


    soup = BeautifulSoup(resp.text, features='html.parser')


    table = soup.find('table', {'id' : 'constituents'})
    tbody = table.find('tbody')

    data = {}
    col_names = []

    ths = tbody.find('tr').find_all('th')

    for idx, th in enumerate(ths):
        if idx == 0 or idx == len(ths)-1:
            data[th.text[:-1]] = []
            col_names.append(th.text[:-1])
        else:
            data[th.text] = []
            col_names.append(th.text)


    trs = tbody.find_all('tr')[1:]

    for tr in trs:
        tds = tr.find_all('td')
        #print(tds)
        for idx, td in enumerate(tds):
            #print(col_names[idx])
            #print(type(data[col_names[idx]]))
            if idx == 0 or idx == len(tds)-1:
                data.get(col_names[idx]).append(td.text[:-1])
            else:
                data.get(col_names[idx]).append(td.text)    

    df = pd.DataFrame(data)
    df.drop(['SEC filings', 'CIK', 'Date first added'], axis=1, inplace=True)
    df.to_excel('~/Documents/S&P-500-list.xlsx')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        print('faat gayi script')
    finally:
        print('Bye Bye')
    