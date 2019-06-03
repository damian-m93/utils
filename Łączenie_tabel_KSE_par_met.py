import pandas as pd
import os

sciezka = 'C:/Users/ca125/Desktop/Łączenie/'
sciezka_srednie = sciezka + 'Średnie/'
sciezka_kse = sciezka + 'KSE/'
nazwa_pliku_zestawienie = 'Zestawienie_zbiorcze_parametry_zapotrzebowanie.xlsx'

tabela_sumaryczna = pd.read_excel(sciezka_srednie + os.listdir(sciezka_srednie)[0], sheet_name='Średnie', index_col=0)

for plik in os.listdir(sciezka_srednie)[1:]:
    tabela_biezaca = pd.read_excel(sciezka_srednie + plik, sheet_name='Średnie', index_col=0)
    tabela_sumaryczna = tabela_sumaryczna.append(tabela_biezaca, ignore_index=False)

tabela_kse = pd.read_excel(sciezka_kse + 'KSE.xlsx')
tabela_kse['Data'] = tabela_kse['Data'] + pd.to_timedelta(tabela_kse['Godzina'] - 1, unit='h')
tabela_kse.set_index(tabela_kse['Data'], inplace=True)
tabela_kse.drop(columns=['Data', 'Godzina', 'WPKD', 'PKD', 'BPKD'], inplace=True)

tabela_sumaryczna = pd.merge(tabela_kse, tabela_sumaryczna, left_index=True, right_index=True, how='outer')
tabela_sumaryczna.to_excel(sciezka + nazwa_pliku_zestawienie)
print(f'Wykonano pomyślnie obliczenia i zapisano plik: {nazwa_pliku_zestawienie}')

