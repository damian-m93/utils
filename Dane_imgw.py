import pandas as pd
import urllib
from bs4 import BeautifulSoup
import os
import zipfile

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('expand_frame_repr', False)

sciezka_pobrane = 'C:/Users/ca125/Desktop/Dane_meteorologiczne_pobrane/'
sciezka_docelowa = 'C:/Users/ca125/Desktop/Dane_meteorologiczne/'

lista_kolumn = [0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 23, 25, 27, 29, 31, 34, 35, 37, 39, 41, 43, 48, 50, 52, 53, 65, 67, 69,
                71, 73, 75, 77, 79, 81, 83, 85, 93, 95, 97]

nazwy_kolumn = ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Godzina',
                'Wysokość podstawy chmur CL CM szyfrowana', 'Wysokość podstawy niższej', 'Wysokość podstawy wyższej',
                'Widzialność', 'Kierunek wiatru', 'Prędkość wiatru', 'Poryw wiatru', 'Temperatura powietrza',
                'Temperatura termometru zwilżonego', 'Wskaźnik lodu', 'Ciśnienie pary wodnej', 'Wilgotność względna',
                'Temperatura punktu rosy', 'Ciśnienie na pozimie stacji', 'Ciśnienie na pozimie morza',
                'Opad za 6 godzin', 'Rodzaj opadu za 6 godzin', 'Pogoda bieżąca', 'Pogoda ubiegła', 'Stan gruntu',
                'Niedosyt wilgotności', 'Usłonecznienie', 'Wystąpienie rosy', 'Poryw maksymalny za okres WW',
                'Godzina wystąpienia porywu', 'Temperatura gruntu -5', 'Temperatura gruntu -10',
                'Temperatura gruntu -20', 'Temperatura gruntu -50', 'Temperatura gruntu -100',
                'Równoważnik wodny śniegu', 'Wysokość pokrywy śnieżnej', 'Wysokość świeżo spadłego śniegu']

nazwy_jednostek = {'Kod stacji': '[-]', 'Nazwa stacji': '[-]', 'Rok': '[-]', 'Miesiąc': '[-]', 'Dzień': '[-]', 'Godzina': '[-]',
                   'Wysokość podstawy chmur CL CM szyfrowana': '[kod]', 'Wysokość podstawy niższej': '[m]',
                   'Wysokość podstawy wyższej': '[m]', 'Widzialność': '[kod]', 'Kierunek wiatru': '[°]',
                   'Prędkość wiatru': '[m/s]', 'Poryw wiatru': '[m/s]', 'Temperatura powietrza': '[°C]',
                   'Temperatura termometru zwilżonego': '[°C]', 'Wskaźnik lodu': '[L/W]', 'Ciśnienie pary wodnej': '[hPa]',
                   'Wilgotność względna': '[%]', 'Temperatura punktu rosy': '[°C]', 'Ciśnienie na pozimie stacji': '[hPa]',
                   'Ciśnienie na pozimie morza': '[hPa]', 'Opad za 6 godzin': '[mm]', 'Rodzaj opadu za 6 godzin': '[kod]',
                   'Pogoda bieżąca': '[kod]', 'Pogoda ubiegła': '[kod]', 'Stan gruntu': '[kod]',
                   'Niedosyt wilgotności': '[hPa]', 'Usłonecznienie': '[-]', 'Wystąpienie rosy': '[0/1]',
                   'Poryw maksymalny za okres WW': '[m/s]', 'Godzina wystąpienia porywu': '[-]',
                   'Temperatura gruntu -5': '[°C]', 'Temperatura gruntu -10': '[°C]', 'Temperatura gruntu -20': '[°C]',
                   'Temperatura gruntu -50': '[°C]', 'Temperatura gruntu -100': '[°C]', 'Równoważnik wodny śniegu': '[mm/cm]',
                   'Wysokość pokrywy śnieżnej': '[cm]', 'Wysokość świeżo spadłego śniegu': '[cm]'}

if len(lista_kolumn) != len(nazwy_kolumn) and len(lista_kolumn) != len(nazwy_jednostek):
    print('Liczba wykorzystywanych kolumn różni się od liczby podanych nazw kolumn lub jednostek!')


def pobierz_pliki():
    """
    Pobiera pliki ze strony imgw w formacie .zip, zapisuje je i wypakowuje ich zawartość do jednego folderu
    """
    base_url = 'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/'
    kod_glowny = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(kod_glowny)
    katalogi_lata = []
    for tr in soup.find_all('tr'):
        try:
            if tr.find('img').get('alt') == '[DIR]':
                katalogi_lata.append(tr.find('a').get('href'))
        except AttributeError:
            continue
    pliki_linki = []
    for katalog in katalogi_lata:
        kod_katalog = urllib.request.urlopen(base_url + katalog)
        soup = BeautifulSoup(kod_katalog)
        for tr in soup.find_all('tr'):
            try:
                if tr.find('a').get('href').endswith('.zip') is True:
                    pliki_linki.append(base_url + katalog + tr.find('a').get('href'))
            except AttributeError:
                continue
    for link in pliki_linki:
        nazwa_zip = link.split('/')[-1]
        urllib.request.urlretrieve(link, nazwa_zip)
        zf = zipfile.ZipFile(nazwa_zip, 'r')
        zf.extractall(sciezka_pobrane)
        zf.close()
        os.remove(nazwa_zip)
    if len(os.listdir(sciezka_pobrane)) == len(pliki_linki):
        print('Tyle samo plików wypakowanych ile plików .zip')
    else:
        print('Inna liczba plików wypakowanych niż plików .zip')


def stworz_pliki(okres_od, okres_do):
    """
    Tworzy puste pliki o podanych nazwach z wypełnionymi datami w podanym zakresie
    Należy podać okresy w formacie str, przykład:
    okres_od = '1960-1-1 00:00'
    okres_do = '2018-12-31 23:00'
    """
    pusta_tabela = pd.DataFrame(columns=['Data'])
    pusta_tabela['Data'] = pd.date_range(start=okres_od, end=okres_do, freq='H')
    nazwy_plikow = ['01_Wysokość podstawy chmur CL CM szyfrowana.xlsx', '02_Wysokość podstawy niższej.xlsx',
                    '03_Wysokość podstawy wyższej.xlsx', '04_Widzialność.xlsx', '05_Kierunek wiatru.xlsx',
                    '06_Prędkość wiatru.xlsx', '07_Poryw wiatru.xlsx', '08_Temperatura powietrza.xlsx',
                    '09_Temperatura termometru zwilżonego.xlsx', '10_Wskaźnik lodu.xlsx',
                    '11_Ciśnienie pary wodnej.xlsx', '12_Wilgotność względna.xlsx', '13_Temperatura punktu rosy.xlsx',
                    '14_Ciśnienie na pozimie stacji.xlsx', '15_Ciśnienie na pozimie morza.xlsx',
                    '16_Opad za 6 godzin.xlsx', '17_Rodzaj opadu za 6 godzin.xlsx', '18_Pogoda bieżąca.xlsx',
                    '19_Pogoda ubiegła.xlsx', '20_Stan gruntu.xlsx', '21_Niedosyt wilgotności.xlsx',
                    '22_Usłonecznienie.xlsx', '23_Wystąpienie rosy.xlsx', '24_Poryw maksymalny za okres WW.xlsx',
                    '25_Godzina wystąpienia porywu.xlsx', '26_Temperatura gruntu -5.xlsx',
                    '27_Temperatura gruntu -10.xlsx', '28_Temperatura gruntu -20.xlsx',
                    '29_Temperatura gruntu -50.xlsx', '30_Temperatura gruntu -100.xlsx',
                    '31_Równoważnik wodny śniegu.xlsx', '32_Wysokość pokrywy śnieżnej.xlsx',
                    '33_Wysokość świeżo spadłego śniegu.xlsx']
    for nazwa_pliku in nazwy_plikow:
        pusta_tabela.to_excel(sciezka_docelowa + nazwa_pliku, index=False)
    print(f'Stworzono pomyślnie wszystkie pliki w ścieżce:\n{sciezka_docelowa}')


def stworz_pliki_rok(rok):
    """
    Tworzy puste pliki o podanych nazwach z wypełnionymi datami dla jednego podanego roku
    Tworzy pliki dla każdego roku w osobnych folderach
    Należy podać rok w formacie str, przykład: '2017'
    """
    os.mkdir(sciezka_docelowa + rok)
    okres_od = rok + '-1-1 00:00'
    okres_do = rok + '-12-31 23:00'
    pusta_tabela = pd.DataFrame(columns=['Data'])
    pusta_tabela['Data'] = pd.date_range(start=okres_od, end=okres_do, freq='H')
    nazwy_plikow = ['01_Wysokość podstawy chmur CL CM szyfrowana.xlsx', '02_Wysokość podstawy niższej.xlsx',
                    '03_Wysokość podstawy wyższej.xlsx', '04_Widzialność.xlsx', '05_Kierunek wiatru.xlsx',
                    '06_Prędkość wiatru.xlsx', '07_Poryw wiatru.xlsx', '08_Temperatura powietrza.xlsx',
                    '09_Temperatura termometru zwilżonego.xlsx', '10_Wskaźnik lodu.xlsx',
                    '11_Ciśnienie pary wodnej.xlsx', '12_Wilgotność względna.xlsx', '13_Temperatura punktu rosy.xlsx',
                    '14_Ciśnienie na pozimie stacji.xlsx', '15_Ciśnienie na pozimie morza.xlsx',
                    '16_Opad za 6 godzin.xlsx', '17_Rodzaj opadu za 6 godzin.xlsx', '18_Pogoda bieżąca.xlsx',
                    '19_Pogoda ubiegła.xlsx', '20_Stan gruntu.xlsx', '21_Niedosyt wilgotności.xlsx',
                    '22_Usłonecznienie.xlsx', '23_Wystąpienie rosy.xlsx', '24_Poryw maksymalny za okres WW.xlsx',
                    '25_Godzina wystąpienia porywu.xlsx', '26_Temperatura gruntu -5.xlsx',
                    '27_Temperatura gruntu -10.xlsx', '28_Temperatura gruntu -20.xlsx',
                    '29_Temperatura gruntu -50.xlsx', '30_Temperatura gruntu -100.xlsx',
                    '31_Równoważnik wodny śniegu.xlsx', '32_Wysokość pokrywy śnieżnej.xlsx',
                    '33_Wysokość świeżo spadłego śniegu.xlsx']
    for nazwa_pliku in nazwy_plikow:
        pusta_tabela.to_excel(sciezka_docelowa + rok + '/' + nazwa_pliku, index=False)
    print(f'Stworzono pomyślnie wszystkie pliki w ścieżce:\n{sciezka_docelowa}{rok}')


def wykonaj_dzialania():
    """
    Wczytuje, obrabia i zapisuje do docelowych skoroszytów odpowiednie dane z pobranych plików
    """
    tabele_docelowe = {}
    for plik_docelowy in os.listdir(sciezka_docelowa):
        tabele_docelowe[plik_docelowy] = pd.read_excel(sciezka_docelowa + plik_docelowy)
    for plik_pobrany in os.listdir(sciezka_pobrane):
        tabela_biezaca = pd.read_csv(sciezka_pobrane + plik_pobrany, encoding='ANSI', header=None,
                                     usecols=lista_kolumn, names=nazwy_kolumn,
                                     parse_dates={'Data': ['Rok', 'Miesiąc', 'Dzień', 'Godzina']},
                                     dtype={'Wysokość podstawy chmur CL CM szyfrowana': object, 'Wskaźnik lodu': object,
                                            'Pogoda bieżąca': object, 'Pogoda ubiegła': object})
        tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'] = pd.to_numeric(
            tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'], errors='coerce')
        tabela_biezaca['Pogoda bieżąca'] = pd.to_numeric(
            tabela_biezaca['Pogoda bieżąca'], errors='coerce')
        tabela_biezaca['Pogoda ubiegła'] = pd.to_numeric(
            tabela_biezaca['Pogoda ubiegła'], errors='coerce')
        for plik_docelowy in os.listdir(sciezka_docelowa):
            nazwa_kolumny = plik_docelowy[3:].split('.')[0]
            tabela_wycieta = tabela_biezaca[['Data', nazwa_kolumny]].copy()
            tabela_wycieta.rename(columns={nazwa_kolumny: tabela_biezaca['Nazwa stacji'][0]}, inplace=True)
            tabele_docelowe[plik_docelowy] = pd.merge(tabele_docelowe[plik_docelowy], tabela_wycieta, on='Data',
                                                      how='outer')
            tabele_docelowe[plik_docelowy].sort_values(by=['Data'], ascending=True, inplace=True)
            print(f'Wykonano działania - {plik_pobrany} - {plik_docelowy}')
    for plik_docelowy, tabela_docelowa in tabele_docelowe.items():
        tabela_docelowa.to_excel(sciezka_docelowa + plik_docelowy, index=False)
        print(f'Zapisano dane - {plik_docelowy}')


def wykonaj_dzialania_rok(rok):
    """
    Wczytuje, obrabia i zapisuje do docelowych skoroszytów odpowiednie dane z pobranych plików
    Rok należy podać w formacie str: 'YYYY'
    W poszczególnych folderach należy umieścić wszystkie pliki z danych lat do obrobienia
    Ta funkcja przygotowana jest dla plików zawierających dane dla jednego roku i tylko jednej stacji
    Nie działa dla 2018 roku (inna struktura plików)
    """
    tabele_docelowe = {}
    for plik_docelowy in os.listdir(sciezka_docelowa + rok + '/'):
        tabele_docelowe[plik_docelowy] = pd.read_excel(sciezka_docelowa + rok + '/' + plik_docelowy)
    for plik_pobrany in os.listdir(sciezka_pobrane + rok + '/'):
        tabela_biezaca = pd.read_csv(sciezka_pobrane + rok + '/' + plik_pobrany, encoding='ANSI', header=None,
                                     usecols=lista_kolumn, names=nazwy_kolumn,
                                     parse_dates={'Data': ['Rok', 'Miesiąc', 'Dzień', 'Godzina']},
                                     dtype={'Wysokość podstawy chmur CL CM szyfrowana': object, 'Wskaźnik lodu': object,
                                            'Pogoda bieżąca': object, 'Pogoda ubiegła': object})
        tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'] = pd.to_numeric(
            tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'], errors='coerce')
        tabela_biezaca['Pogoda bieżąca'] = pd.to_numeric(
            tabela_biezaca['Pogoda bieżąca'], errors='coerce')
        tabela_biezaca['Pogoda ubiegła'] = pd.to_numeric(
            tabela_biezaca['Pogoda ubiegła'], errors='coerce')
        for plik_docelowy in os.listdir(sciezka_docelowa + rok + '/'):
            nazwa_kolumny = plik_docelowy[3:].split('.')[0]
            tabela_wycieta = tabela_biezaca[['Data', nazwa_kolumny]].copy()
            tabela_wycieta.rename(columns={nazwa_kolumny: tabela_biezaca['Nazwa stacji'][0]}, inplace=True)
            tabele_docelowe[plik_docelowy] = pd.merge(tabele_docelowe[plik_docelowy], tabela_wycieta, on='Data',
                                                      how='outer')
            tabele_docelowe[plik_docelowy].sort_values(by=['Data'], ascending=True, inplace=True)
            print(f'Wykonano działania - {rok} - {plik_pobrany} - {plik_docelowy}')
    for plik_docelowy, tabela_docelowa in tabele_docelowe.items():
        tabela_docelowa.to_excel(sciezka_docelowa + rok + '/' + plik_docelowy, index=False)
        print(f'Zapisano dane - {rok} - {plik_docelowy}')


def wykonaj_dzialania_mies(rok):
    """
    Wczytuje, obrabia i zapisuje do docelowych skoroszytów odpowiednie dane z pobranych plików
    Rok należy podać w formacie str: 'YYYY'
    W poszczególnych folderach należy umieścić wszystkie pliki z danych lat do obrobienia
    Ta funkcja przygotowana jest dla plików zawierających dane dla jednego roku i tylko jednej stacji
    Nie działa dla 2018 roku (inna struktura plików)
    """
    tabele_docelowe_stacje = {}
    tabele_docelowe = {}
    for plik_docelowy in os.listdir(sciezka_docelowa + rok + '/'):
        tabele_docelowe[plik_docelowy] = pd.read_excel(sciezka_docelowa + rok + '/' + plik_docelowy)
    for plik_pobrany in os.listdir(sciezka_pobrane + rok + '/'):
        tabela_biezaca = pd.read_csv(sciezka_pobrane + rok + '/' + plik_pobrany, encoding='ANSI', header=None,
                                     usecols=lista_kolumn, names=nazwy_kolumn,
                                     parse_dates={'Data': ['Rok', 'Miesiąc', 'Dzień', 'Godzina']},
                                     dtype={'Wysokość podstawy chmur CL CM szyfrowana': object, 'Wskaźnik lodu': object,
                                            'Pogoda bieżąca': object, 'Pogoda ubiegła': object})
        tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'] = pd.to_numeric(
            tabela_biezaca['Wysokość podstawy chmur CL CM szyfrowana'], errors='coerce')
        tabela_biezaca['Pogoda bieżąca'] = pd.to_numeric(
            tabela_biezaca['Pogoda bieżąca'], errors='coerce')
        tabela_biezaca['Pogoda ubiegła'] = pd.to_numeric(
            tabela_biezaca['Pogoda ubiegła'], errors='coerce')
        lista_stacji = set(tabela_biezaca['Nazwa stacji'])
        for nazwa_stacji in lista_stacji:
            if nazwa_stacji not in tabele_docelowe_stacje.keys():
                tabele_docelowe_stacje[nazwa_stacji] = pd.DataFrame()
            warunek_stacje = tabela_biezaca['Nazwa stacji'] == nazwa_stacji
            tabele_docelowe_stacje[nazwa_stacji] = tabele_docelowe_stacje[nazwa_stacji].append(
                tabela_biezaca[warunek_stacje])
            print(f'Stworzono pierwsze tabele - {rok} - {plik_pobrany} - {nazwa_stacji}')
    for nazwa_stacji, tabela_stacja in tabele_docelowe_stacje.items():
        for plik_docelowy in os.listdir(sciezka_docelowa + rok + '/'):
            nazwa_kolumny = plik_docelowy[3:].split('.')[0]
            tabela_wycieta = tabela_stacja[['Data', nazwa_kolumny]].copy()
            tabela_wycieta.rename(columns={nazwa_kolumny: nazwa_stacji}, inplace=True)
            tabele_docelowe[plik_docelowy] = pd.merge(tabele_docelowe[plik_docelowy], tabela_wycieta, on='Data',
                                                      how='outer')
            tabele_docelowe[plik_docelowy].sort_values(by=['Data'], ascending=True, inplace=True)
            print(f'Wykonano działania - {rok} - {nazwa_stacji} - {plik_docelowy}')
    for plik_docelowy, tabela_docelowa in tabele_docelowe.items():
        tabela_docelowa.to_excel(sciezka_docelowa + rok + '/' + plik_docelowy, index=False)
        print(f'Zapisano dane - {rok} - {plik_docelowy}')


def wyznacz_srednie():
    """
    Tworzy plik z wyznaczonymi średnimi dla poszczególnych parametrów oraz różnicami względem stacji z Katowic
    """
    tabela_srednie = pd.DataFrame(columns=['Data'])
    tabela_srednie['Data'] = pd.date_range(start='1960-1-1 00:00', end='2018-12-31 23:00', freq='H')
    tabela_katowice = pd.DataFrame(columns=['Data'])
    tabela_katowice['Data'] = pd.date_range(start='1960-1-1 00:00', end='2018-12-31 23:00', freq='H')
    for plik in os.listdir(sciezka_docelowa):
        nazwa_kolumny = plik[3:].split('.')[0]
        tabela_biezaca = pd.read_excel(sciezka_docelowa + plik)
        tabela_biezaca['Średnia'] = tabela_biezaca.mean(axis=1, skipna=True)
        tabela_biezaca['Średnia'] = tabela_biezaca['Średnia'].round(decimals=3)
        tabela_srednie = pd.merge(tabela_srednie, tabela_biezaca[['Data', 'Średnia']], on='Data', how='outer')
        tabela_srednie.rename(columns={'Średnia': nazwa_kolumny}, inplace=True)
        tabela_srednie.sort_values(by=['Data'], ascending=True, inplace=True)
        tabela_katowice = pd.merge(tabela_katowice, tabela_biezaca[['Data', 'KATOWICE']], on='Data', how='outer')
        tabela_katowice.rename(columns={'KATOWICE': nazwa_kolumny}, inplace=True)
        tabela_katowice.sort_values(by=['Data'], ascending=True, inplace=True)
        tabela_roznica = tabela_katowice.set_index('Data').sub(tabela_srednie.set_index('Data')).reset_index()
        print(f'Wykonano dla pliku - {plik}')
    for tabela in [tabela_srednie, tabela_katowice, tabela_roznica]:
        for nazwa in tabela.columns[1:]:
            tabela.rename(columns={nazwa: nazwa + ' ' + nazwy_jednostek[nazwa]}, inplace=True)
    nazwa_pliku = 'Średnie_godzinowe.xlsx'
    writer = pd.ExcelWriter(sciezka_docelowa + nazwa_pliku)
    tabela_srednie.to_excel(writer, 'Średnie', index=None)
    tabela_katowice.to_excel(writer, 'Katowice', index=None)
    tabela_roznica.to_excel(writer, 'Różnica', index=None)
    writer.save()
    print(f'Zapisano dane - {sciezka_docelowa + nazwa_pliku}')


def wyznacz_srednie_rok(rok):
    """
    Tworzy plik z wyznaczonymi średnimi dla poszczególnych parametrów oraz różnicami względem stacji z Katowic
    Ta funkcja przygotowana jest dla plików zawierające dane z jednego roku i wszystkich stacji
    Rok należy podać w formacie str: 'YYYY'
    """
    okres_od = rok + '-1-1 00:00'
    okres_do = rok + '-12-31 23:00'
    tabela_srednie = pd.DataFrame(columns=['Data'])
    tabela_srednie['Data'] = pd.date_range(start=okres_od, end=okres_do, freq='H')
    tabela_katowice = pd.DataFrame(columns=['Data'])
    tabela_katowice['Data'] = pd.date_range(start=okres_od, end=okres_do, freq='H')
    for plik in os.listdir(sciezka_docelowa + rok + '/'):
        nazwa_kolumny = plik[3:].split('.')[0]
        tabela_biezaca = pd.read_excel(sciezka_docelowa + rok + '/' + plik)
        tabela_biezaca['Średnia'] = tabela_biezaca.mean(axis=1, skipna=True)
        tabela_biezaca['Średnia'] = tabela_biezaca['Średnia'].round(decimals=3)
        tabela_srednie = pd.merge(tabela_srednie, tabela_biezaca[['Data', 'Średnia']], on='Data', how='outer')
        tabela_srednie.rename(columns={'Średnia': nazwa_kolumny}, inplace=True)
        tabela_srednie.sort_values(by=['Data'], ascending=True, inplace=True)
        tabela_katowice = pd.merge(tabela_katowice, tabela_biezaca[['Data', 'KATOWICE']], on='Data', how='outer')
        tabela_katowice.rename(columns={'KATOWICE': nazwa_kolumny}, inplace=True)
        tabela_katowice.sort_values(by=['Data'], ascending=True, inplace=True)
        tabela_roznica = tabela_katowice.set_index('Data').sub(tabela_srednie.set_index('Data')).reset_index()
        print(f'Wykonano dla pliku - {rok} - {plik}')
    for tabela in [tabela_srednie, tabela_katowice, tabela_roznica]:
        for nazwa in tabela.columns[1:]:
            tabela.rename(columns={nazwa: nazwa + ' ' + nazwy_jednostek[nazwa]}, inplace=True)
    nazwa_pliku = rok + '_Średnie_godzinowe_parametrów.xlsx'
    writer = pd.ExcelWriter(sciezka_docelowa + rok + '/' + nazwa_pliku)
    tabela_srednie.to_excel(writer, 'Średnie', index=None)
    tabela_katowice.to_excel(writer, 'Katowice', index=None)
    tabela_roznica.to_excel(writer, 'Różnica', index=None)
    writer.save()
    print(f'Zapisano dane - {sciezka_docelowa}{rok}/{nazwa_pliku}')

