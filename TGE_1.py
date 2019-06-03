# Otwiera wszystkie skoroszyty w folderze, obrabia je i tworzy sumaryczną tabelę i zapisuje do pliku .xlsx
# Z racji tylko 2 lat ręcznie w dwóch plikach usunięto godzinę '2a'

import pandas as pd
import os

tabela_zbiorcza = pd.DataFrame(columns=['Data', 'Godzina', 'Kurs średni ważony', 'Wolumen'])
sciezka = 'C:/Users/ca125/Desktop/TGE/'
sciezka_pobrane = sciezka + 'Pobrane_pliki/'

for plik in os.listdir(sciezka_pobrane):
    try:
        tabela = pd.read_excel(sciezka_pobrane + plik, sheet_name='WYNIKI', usecols='B, C, D')
        tabela.dropna(how='any', inplace=True)
        tabela.columns = ['Data', 'Kurs średni ważony', 'Wolumen']
        tabela['Godzina'] = tabela.apply(lambda row: row['Data'][-2:], axis=1)
        tabela['Data'] = tabela.apply(lambda row: row['Data'][:-4], axis=1)
        tabela['Data'] = pd.to_datetime(tabela['Data'], format='%d-%m-%y')
        tabela['Kurs średni ważony'] = tabela['Kurs średni ważony'].astype(float)
        tabela['Wolumen'] = tabela['Wolumen'].astype(float)
        tabela['Godzina'] = tabela['Godzina'].astype(int)
        tabela = tabela[['Data', 'Godzina', 'Kurs średni ważony', 'Wolumen']]
        tabela_zbiorcza = pd.merge(tabela_zbiorcza, tabela, how='outer')
    except BaseException as error:
        print('Błąd przy pliku ' + plik)
        print(error)
        continue

tabela_zbiorcza.sort_values(by=['Data', 'Godzina'], ascending=True, inplace=True)
tabela_zbiorcza.to_excel(sciezka + 'TGE_RDN.xlsx', index=False)
