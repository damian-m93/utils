import pandas as pd
from urllib import error as httperr
from datetime import datetime as dt

lista_bledow = []


def cro(data_od, data_do):
    """
    :param data_od: dt(YYYY, M, D)
    :param data_do: dt(YYYY, M, D)
    """
    nazwa_pliku = 'cro.xlsx'
    base_url = 'https://www.pse.pl/getcsv/-/export/csv/CENY_ROZL_RB/data/'
    tabela_cro = pd.DataFrame(columns=['Data', 'Godzina', 'CRO'])
    tabela_cro.set_index(['Data', 'Godzina'], inplace=True)
    okres = pd.date_range(data_od, data_do)
    for data in okres:
        adres = base_url + data.strftime('%Y%m%d')
        try:
            cro_dzien = pd.read_csv(adres, encoding='ISO-8859-1', sep=';', usecols=['Data', 'Godzina', 'CRO'],
                                    parse_dates=['Data'], decimal=',')
        except httperr.HTTPError:
            print(f'Błąd - niedostępny adres - {adres}')
            lista_bledow.append(f'(CRO) Błąd - niedostępny adres - {adres}')
            continue
        try:
            cro_dzien['Godzina'] = cro_dzien['Godzina'].astype(int)
        except ValueError:
            cro_dzien['Godzina'] = pd.to_numeric(cro_dzien['Godzina'], errors='coerce')
            cro_dzien.dropna(axis=0, how='any', inplace=True)
            cro_dzien['Godzina'] = cro_dzien['Godzina'].astype(int)
            lista_bledow.append('(CRO) Usunięto godzinę 2A w dniu ' + data.strftime('%Y-%m-%d'))
        cro_dzien.set_index(['Data', 'Godzina'], inplace=True)
        try:
            tabela_cro = tabela_cro.append(cro_dzien, ignore_index=False)
            print('(CRO) OK - ' + data.strftime('%Y-%m-%d'))
        except BaseException as error:
            print('Błąd w dniu - ' + data.strftime('%Y-%m-%d') + ': ' + str(error))
            lista_bledow.append('(CRO) Błąd w dniu - ' + data.strftime('%Y-%m-%d') + ': ' + str(error))
            continue
    tabela_cro.reset_index(inplace=True)
    tabela_cro.to_excel(nazwa_pliku, index=None)
    print('----------')
    for i in lista_bledow:
        print(i)


def zrb(data_od, data_do):
    """
    Na stronie dane dostępne od 2016 roku
    :param data_od: dt(YYYY, M, D)
    :param data_do: dt(YYYY, M, D)
    """
    nazwa_pliku = 'zrb.xlsx'
    base_url = 'https://www.pse.pl/getcsv/-/export/csv/PL_ZRB/data/'
    tabela_zrb = pd.DataFrame(columns=['Data', 'Godzina', 'ZRB BPKD/BO'])
    tabela_zrb.set_index(['Data', 'Godzina'], inplace=True)
    okres = pd.date_range(data_od, data_do)
    for data in okres:
        adres = base_url + data.strftime('%Y%m%d')
        try:
            zrb_dzien = pd.read_csv(adres, encoding='ISO-8859-1', sep=';', usecols=['Data', 'Godzina', 'ZRB BPKD/BO'],
                                    parse_dates=['Data'], decimal=',')
        except httperr.HTTPError:
            print(f'Błąd - niedostępny adres - {adres}')
            lista_bledow.append(f'(ZRB) Błąd - niedostępny adres - {adres}')
            continue
        try:
            zrb_dzien['Godzina'] = zrb_dzien['Godzina'].astype(int)
        except ValueError:
            zrb_dzien['Godzina'] = pd.to_numeric(zrb_dzien['Godzina'], errors='coerce')
            zrb_dzien.dropna(axis=0, how='any', inplace=True)
            zrb_dzien['Godzina'] = zrb_dzien['Godzina'].astype(int)
            lista_bledow.append('(ZRB) Usunięto godzinę 2A w dniu ' + data.strftime('%Y-%m-%d'))
        zrb_dzien.set_index(['Data', 'Godzina'], inplace=True)
        try:
            tabela_zrb = tabela_zrb.append(zrb_dzien, ignore_index=False)
            print('(ZRB) OK - ' + data.strftime('%Y-%m-%d'))
        except BaseException as error:
            print('Błąd w dniu - ' + data.strftime('%Y-%m-%d') + ': ' + str(error))
            lista_bledow.append('(ZRB) Błąd w dniu - ' + data.strftime('%Y-%m-%d') + ': ' + str(error))
            continue
    tabela_zrb.reset_index(inplace=True)
    tabela_zrb.to_excel(nazwa_pliku, index=None)
    print('----------')
    for i in lista_bledow:
        print(i)


zrb(dt(2016, 1, 1), dt(2018, 12, 31))
