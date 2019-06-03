import pandas as pd
import os


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


sciezka = 'C:/Users/ca125/Desktop/Stopniodni/'

for plik in os.listdir(sciezka):
    df = pd.read_excel(sciezka + plik)
    tabela_srednie = df.groupby(df['Data'].dt.date).mean()
    tabela_srednie['Stopniodni grzewcze [18 °C Baza]'] = tabela_srednie['Temperatura powietrza [°C]'].apply(
        stopniodni_grzewcze)
    tabela_srednie['Stopniodni chłodnicze [18 °C Baza]'] = tabela_srednie['Temperatura powietrza [°C]'].apply(
        stopniodni_chlodnicze)
    tabela_srednie.index = pd.to_datetime(tabela_srednie.index)
    df = df.join(tabela_srednie['Stopniodni grzewcze [18 °C Baza]'], on='Data')
    df = df.join(tabela_srednie['Stopniodni chłodnicze [18 °C Baza]'], on='Data')
    df['Stopniodni grzewcze [18 °C Baza]'].fillna(method='ffill', inplace=True)
    df['Stopniodni chłodnicze [18 °C Baza]'].fillna(method='ffill', inplace=True)
    df.to_excel(sciezka + 'Stopniodni_' + plik, index=False)
    print(f'Pomyślnie wykonano działania oraz zapisano plik: {plik}')

