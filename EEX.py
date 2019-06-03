import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

sciezka_docelowa = 'C:/Users/Damian/Desktop/EEX/'
nazwa_pliku = 'EEX.xlsx'

driver = webdriver.Chrome(executable_path=r'C:/Users/Damian/Desktop/EEX/chromedriver.exe')

base_url = 'https://www.eex.com/en/market-data/power/spot-market/auction#!/'
zakres_dat = pd.date_range(start='2016-01-01', end='2018-12-31', freq='d')

tabela_wynikowa = pd.DataFrame()

for data in zakres_dat:
    try:
        rok = str(data.year)
        miesiac = str(data.month)
        if len(miesiac) == 1:
            miesiac = str(0) + miesiac
        dzien = str(data.day)
        if len(dzien) == 1:
            dzien = str(0) + dzien
        url = base_url + f'{rok}/{miesiac}/{dzien}'
        driver.get(url)
        time.sleep(5)
        kod_zrodlowy = driver.page_source
        soup = BeautifulSoup(kod_zrodlowy, "html.parser")
        tabela = pd.read_html(str(soup.find_all('table')[1]))[0]
        tabela.drop(columns=['Unnamed: 2'], inplace=True)
        tabela.rename(columns={'Hour': 'Godzina', 'Price': 'ELIX [EUR/MWh]'}, inplace=True)
        tabela['Godzina'] = tabela['Godzina'].apply(lambda row: row[:2])
        tabela.index = data + tabela['Godzina'].astype('timedelta64[h]')
        tabela.drop(columns=['Godzina'], inplace=True)
        tabela.index = pd.MultiIndex.from_arrays([tabela.index.date, tabela.index.hour], names=['Data', 'Godzina'])
        tabela_wynikowa = tabela_wynikowa.append(tabela, sort=False)
        print(f'Wykonano dla daty: {data}')
    except BaseException as error:
        print(f'Błąd przy dacie - {data}')
        print(error)
        print('---------')
driver.close()

tabela_wynikowa.sort_values(by=['Data', 'Godzina'], ascending=True, inplace=True)
tabela_wynikowa.reset_index(inplace=True)
tabela_wynikowa.to_excel(sciezka_docelowa + nazwa_pliku, index=False)

