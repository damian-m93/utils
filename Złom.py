import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument('user-data-dir=C:\\Users\\Damian\\AppData\\Local\\Google\\Chrome\\User Data')
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options,
                          executable_path=r'C:/Users/Damian/Desktop/chromedriver.exe')

driver.get('https://zlom.info.pl/')
driver.find_element_by_name("username").send_keys('xxxxxxxxxx')
driver.find_element_by_name("password").send_keys('xxxxxxxxxx')
driver.find_element_by_name("Submit").click()


def stworz_liste_linkow():
    base_url = 'https://zlom.info.pl/wskazniki-cen-zlomu/ceny-zlomu.html?start='
    base_url_ceny = 'https://zlom.info.pl'
    linki = []
    for i in range(0, 430, 10):
        url = base_url + str(i)
        driver.get(url)
        kod_zrodlowy = driver.page_source
        soup = BeautifulSoup(kod_zrodlowy, "html.parser")
        for a in soup.find_all('a', attrs={'class': 'k2ReadMore'}):
            linki.append(base_url_ceny + a.get('href'))
    return linki


def stworz_liste_tabel():
    lista_tabel = {}
    for link in lista_linkow:
        while True:
            try:
                driver.get(link)
                kod_zrodlowy = driver.page_source
                soup = BeautifulSoup(kod_zrodlowy, "html.parser")
                tabela = pd.read_html(str(soup.find_all('table')[0]))[0].dropna().transpose()
                tabela = tabela.rename(columns=tabela.iloc[0]).drop(tabela.index[0])
                nazwa_tabeli = str(link.split('-')[-2] + '_' + link.split('-')[-3])
                tabela.rename(index={1: nazwa_tabeli}, inplace=True)
                lista_tabel[nazwa_tabeli] = tabela
                print(f'OK - {link}')
            except BaseException as error:
                print(error)
                continue
            break
    print('Pomyślnie stworzono listę wszystkich tabel')
    return lista_tabel


try:
    lista_linkow = stworz_liste_linkow()
    print('Pomyślnie stworzono listę linków')
except BaseException as error:
    print(error)

tabele = stworz_liste_tabel()

df = pd.DataFrame()

for tabela in tabele.values():
    df = df.append(tabela, sort=False)
print('Pomyślnie połączono tabele')
df.to_excel('C:/Users/Damian/Desktop/Ceny_złomu_przed_obróbką.xlsx')
print('Pomyślnie zapisano plik przed obróbką')

nazwy_kolumn = df.columns
for nazwa in nazwy_kolumn:
    try:
        df[nazwa] = df[nazwa].apply(lambda x: x.split('\xa0')[0] if pd.notnull(x) else x)
    except BaseException as error:
        print(error)
        continue
print('Koniec działania split (twarda spacja)')
for nazwa in nazwy_kolumn:
    try:
        df[nazwa] = df[nazwa].apply(lambda x: x.split(' ')[0] if pd.notnull(x) else x)
    except BaseException as error:
        print(error)
        continue
print('Koniec działania split (zwykła spacja)')
for nazwa in nazwy_kolumn:
    try:
        df[nazwa] = df[nazwa].apply(lambda x: x.replace(',', '.') if pd.notnull(x) else x)
    except BaseException as error:
        print(error)
        continue
print('Koniec działania replace')
for nazwa in nazwy_kolumn:
    try:
        df[nazwa] = pd.to_numeric(df[nazwa])
    except BaseException as error:
        print(error)
        continue
print('Koniec działania to_numeric')
print('Wykonano wszystkie operacje na tabeli wynikowej')

df.to_excel('C:/Users/Damian/Desktop/Ceny_złomu_po_obróbce.xlsx')
print('Pomyślnie wyeksportowano tabelę do pliku')
