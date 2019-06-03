import pandas as pd

sciezka = 'C:/Users/ca125/Desktop/Łączenie/'
nazwa_pliku_zestawienie = 'Zestawienie_zbiorcze_rynek_gieldy_zapotrzebowanie.xlsx'

# Tworzy tabelę wynikową z odpowiednim zakresem dat

tabela = pd.DataFrame({'Data': pd.date_range(start='2009-1-1 00:00', end='2018-12-31 23:00', freq='h')})
tabela['Data'] = pd.to_datetime(tabela['Data'])
tabela.set_index(['Data'], inplace=True)
tabela.index = pd.MultiIndex.from_arrays([tabela.index.date, tabela.index.hour], names=['Data', 'Godzina'])
print('Pomyślnie stworzono tabelę wynikową')

# Tabela zapotrzebowanie KSE

plik = 'KSE.xlsx'
tabela_kse = pd.read_excel(sciezka + plik)
tabela_kse.index = tabela_kse['Data'] + pd.to_timedelta(tabela_kse['Godzina'] - 1, unit='h')
tabela_kse.index = pd.MultiIndex.from_arrays([tabela_kse.index.date, tabela_kse.index.hour], names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela CRO

plik = 'CRO.xlsx'
tabela_cro = pd.read_excel(sciezka + plik)
tabela_cro.index = tabela_cro['Data'] + pd.to_timedelta(tabela_cro['Godzina'] - 1, unit='h')
tabela_cro.index = pd.MultiIndex.from_arrays([tabela_cro.index.date, tabela_cro.index.hour], names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela ZRB

plik = 'ZRB.xlsx'
tabela_zrb = pd.read_excel(sciezka + plik)
tabela_zrb.index = tabela_zrb['Data'] + pd.to_timedelta(tabela_zrb['Godzina'] - 1, unit='h')
tabela_zrb.index = pd.MultiIndex.from_arrays([tabela_zrb.index.date, tabela_zrb.index.hour], names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela TGE

plik = 'TGE_RDN.xlsx'
tabela_tge = pd.read_excel(sciezka + plik)
tabela_tge.index = tabela_tge['Data'] + pd.to_timedelta(tabela_tge['Godzina'] - 1, unit='h')
tabela_tge.index = pd.MultiIndex.from_arrays([tabela_tge.index.date, tabela_tge.index.hour], names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela Brent

plik = 'BRENT.xlsx'
tabela_brent = pd.read_excel(sciezka + plik)
tabela_brent.index = tabela_brent['Data'] + pd.to_timedelta(tabela_brent['Godzina'], unit='h')
tabela_brent.index = pd.MultiIndex.from_arrays([tabela_brent.index.date, tabela_brent.index.hour],
                                               names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela EEX

plik = 'EEX.xlsx'
tabela_eex = pd.read_excel(sciezka + plik)
tabela_eex.index = tabela_eex['Data'] + pd.to_timedelta(tabela_eex['Godzina'], unit='h')
tabela_eex.index = pd.MultiIndex.from_arrays([tabela_eex.index.date, tabela_eex.index.hour],
                                             names=['Data', 'Godzina'])
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela Nordpool_ceny

plik = 'Nordpool_ceny.xlsx'
tabela_np_ceny = pd.read_excel(sciezka + plik)
tabela_np_ceny.index = tabela_np_ceny['Data'] + pd.to_timedelta(tabela_np_ceny['Godzina'], unit='h')
tabela_np_ceny.index = pd.MultiIndex.from_arrays([tabela_np_ceny.index.date, tabela_np_ceny.index.hour],
                                                 names=['Data', 'Godzina'])
tabela_np_ceny.drop(columns=['Data', 'Godzina'], inplace=True)
tabela_np_ceny = tabela_np_ceny.add_prefix('Nordpool_P_')
tabela_np_ceny = tabela_np_ceny.add_suffix(' [EUR/MWh]')
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Tabela Nordpool_wolumeny

plik = 'Nordpool_wolumeny.xlsx'
tabela_np_vol = pd.read_excel(sciezka + plik)
tabela_np_vol.index = tabela_np_vol['Data'] + pd.to_timedelta(tabela_np_vol['Godzina'], unit='h')
tabela_np_vol.index = pd.MultiIndex.from_arrays([tabela_np_vol.index.date, tabela_np_vol.index.hour],
                                                names=['Data', 'Godzina'])
tabela_np_vol.drop(columns=['Data', 'Godzina'], inplace=True)
tabela_np_vol = tabela_np_vol.add_prefix('Nordpool_V_')
tabela_np_vol = tabela_np_vol.add_suffix(' [MWh]')
print(f'Pomyślnie przygotowano tabelę - {plik}')

# Dodaje wszystkie kolumny do tabeli wynikowej

tabela = tabela.join(tabela_kse['Wykonanie KSE'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_cro['CRO'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_zrb['ZRB BPKD/BO'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_tge['Kurs średni ważony'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_tge['Wolumen'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_brent['BRENT SPOT Price FOB [Dollars/Barrel]'], on=['Data', 'Godzina'])
tabela.rename(columns={'Wykonanie KSE': 'Wykonanie KSE [MW]',
                       'CRO': 'CRO [zł/MWh]',
                       'ZRB BPKD/BO': 'ZRB BPKD/BO [MW]',
                       'Kurs średni ważony': 'TGE, kurs średni ważony [PLN]',
                       'Wolumen': 'TGE, wolumen [MWh]'},
              inplace=True)
tabela = tabela.join(tabela_eex['ELIX [EUR/MWh]'], on=['Data', 'Godzina'])
tabela = tabela.join(tabela_np_ceny, on=['Data', 'Godzina'])
tabela = tabela.join(tabela_np_vol, on=['Data', 'Godzina'])
print('Pomyślnie połączono wszystkie tabele')

# Zapisuje do pliku tabelę wynikową

tabela.reset_index(inplace=True)
tabela.to_excel(sciezka + nazwa_pliku_zestawienie, index=False)
print(f'Pomyślnie zapisano tabelę wynikową do pliku: {nazwa_pliku_zestawienie}')
