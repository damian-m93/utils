import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option('expand_frame_repr', False)

tabele = {}
sciezka = 'C:/Users/ca125/Desktop/Stopniodni/'


def stopniodni_grzewcze(temperatura_srednia_dzienna):
    temperatura_bazowa = 18
    if temperatura_srednia_dzienna <= temperatura_bazowa:
        return temperatura_bazowa - temperatura_srednia_dzienna
    else:
        return 0


def stopniodni_chlodnicze(temperatura_srednia_dzienna):
    temperatura_bazowa = 18
    if temperatura_srednia_dzienna > temperatura_bazowa:
        return temperatura_srednia_dzienna - temperatura_bazowa
    else:
        return 0


for plik in os.listdir(sciezka):
    rok = plik[:4]
    tabele[rok] = pd.read_excel(sciezka + plik, sheet_name='Średnie')
    tabela_srednie = tabele[rok].groupby([tabele[rok]['Data'].dt.date]).mean()
    tabela_srednie['Stopniodni grzewcze [18 °C Baza]'] = tabela_srednie['Temperatura powietrza [°C]'].apply(
        stopniodni_grzewcze)
    tabela_srednie['Stopniodni chłodnicze [18 °C Baza]'] = tabela_srednie['Temperatura powietrza [°C]'].apply(
        stopniodni_chlodnicze)
    tabela_srednie.index = pd.to_datetime(tabela_srednie.index)
    tabele[rok] = tabele[rok].join(tabela_srednie['Stopniodni grzewcze [18 °C Baza]'], on='Data')
    tabele[rok] = tabele[rok].join(tabela_srednie['Stopniodni chłodnicze [18 °C Baza]'], on='Data')
    tabele[rok]['Stopniodni grzewcze [18 °C Baza]'].fillna(method='ffill', inplace=True)
    tabele[rok]['Stopniodni chłodnicze [18 °C Baza]'].fillna(method='ffill', inplace=True)
    tabele[rok].to_excel(sciezka + plik, sheet_name='Średnie', index=False)
    print(f'Pomyślnie wykonano działania oraz zapisano plik: {plik}')

