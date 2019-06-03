import pandas as pd
import os

sciezka = 'C:/Users/ca125/Desktop/Nordpool/'
sciezka_ceny = sciezka + 'Ceny_pobrane_pliki/'
sciezka_wolumeny = sciezka + 'Wolumeny_pobrane_pliki/'
plik_wynikowy_ceny = 'Nordpool_ceny.xlsx'
plik_wynikowy_wolumeny = 'Nordpool_wolumeny.xlsx'


def nordpool_ceny():
    tabela_ceny = pd.DataFrame()
    for plik in os.listdir(sciezka_ceny):
        tabela_biezaca = pd.read_excel(sciezka_ceny + plik, header=2)
        tabela_biezaca.rename(columns={'Hours': 'Godzina'}, inplace=True)
        tabela_biezaca['Godzina'] = tabela_biezaca['Godzina'].apply(lambda row: row[:2])
        tabela_biezaca.index = pd.to_datetime(tabela_biezaca.index) + tabela_biezaca['Godzina'].astype('timedelta64[h]')
        tabela_biezaca.drop(columns=['Godzina'], inplace=True)
        tabela_biezaca.index = pd.MultiIndex.from_arrays([tabela_biezaca.index.date, tabela_biezaca.index.hour],
                                                         names=['Data', 'Godzina'])
        tabela_ceny = tabela_ceny.append(tabela_biezaca, sort=False)
    try:
        tabela_ceny.drop(columns=['FRE'], inplace=True)
        print('Usunięto kolumnę "FRE"')
    except BaseException:
        print('Nie znaleziono kolumny "FRE"')
    tabela_ceny.sort_values(by=['Data', 'Godzina'], ascending=True, inplace=True)
    tabela_ceny.reset_index(inplace=True)
    tabela_ceny.to_excel(sciezka + plik_wynikowy_ceny, index=False)


def nordpool_wolumeny():
    tabela_wolumeny = pd.DataFrame()
    for plik in os.listdir(sciezka_wolumeny):
        tabela_biezaca = pd.read_excel(sciezka_wolumeny + plik, header=2)
        tabela_biezaca.rename(columns={'Hours': 'Godzina'}, inplace=True)
        tabela_biezaca['Godzina'] = tabela_biezaca['Godzina'].apply(lambda row: row[:2])
        tabela_biezaca.index = pd.to_datetime(tabela_biezaca.index) + tabela_biezaca['Godzina'].astype('timedelta64[h]')
        tabela_biezaca.drop(columns=['Godzina'], inplace=True)
        tabela_biezaca.index = pd.MultiIndex.from_arrays([tabela_biezaca.index.date, tabela_biezaca.index.hour],
                                                         names=['Data', 'Godzina'])
        tabela_wolumeny = tabela_wolumeny.append(tabela_biezaca, sort=False)
    try:
        tabela_wolumeny.drop(columns=['FRE Buy', 'FRE Sell'], inplace=True)
        print('Usunięto kolumny "FRE Buy" oraz "FRE Sell"')
    except BaseException:
        print('Nie znaleziono kolumny "FRE Buy" oraz "FRE Sell"')
    tabela_wolumeny.sort_values(by=['Data', 'Godzina'], ascending=True, inplace=True)
    tabela_wolumeny.reset_index(inplace=True)
    tabela_wolumeny.to_excel(sciezka + plik_wynikowy_wolumeny, index=False)


nordpool_ceny()
nordpool_wolumeny()
