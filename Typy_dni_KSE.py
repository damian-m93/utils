import pandas as pd
from datetime import date
import holidays

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 60)
pd.set_option('expand_frame_repr', False)

sciezka = 'C:/Users/ca125/Desktop/'
nazwa_pliku_kse = 'KSE.xlsx'

pl_holidays = holidays.Polish(years=[rok for rok in range(2009, 2019)])
pl_holidays.append({date(2018, 11, 12): 'Narodowe Święto Niepodległości (drugi dzień)'})


def czy_weekend(dzien):
    dni_weekend = ['Sa', 'Su']
    if dzien in dni_weekend:
        return 'W'
    else:
        return 'R'


def czy_swieto(dzien):
    if dzien.month == 12 and dzien.day == 24:
        return 'Wig'
    elif dzien in pl_holidays:
        return 'S'
    else:
        return 'NS'


df_kse = pd.read_excel(sciezka + nazwa_pliku_kse)
df_kse.index = df_kse['Data'] + pd.to_timedelta(df_kse['Godzina'] - 1, unit='h')
df_kse.drop(columns=['Data', 'Godzina'], inplace=True)
df_kse.index.name = 'Data'
df_kse['Dzień'] = df_kse.index.day_name()
df_kse['Dzień'] = df_kse['Dzień'].apply(lambda row: row[:2])
df_kse['Typ dnia [R/W]'] = df_kse['Dzień'].apply(czy_weekend)
df_kse['Święto [S/NS/Wig]'] = df_kse.index.date
df_kse['Święto [S/NS/Wig]'] = df_kse['Święto [S/NS/Wig]'].apply(czy_swieto)

nazwy_kolumn = ['Data', 'Godzina', 'Dzień', 'Typ dnia [R/W]', 'Święto [S/NS/Wig]', 'WPKD', 'PKD', 'BPKD',
                'Wykonanie KSE']


def wszystkie_lata():
    nazwa_pliku_docelowego = '_Typy_dni_KSE_Zestawienie.xlsx'
    lista_godzin = [godzina for godzina in range(24)]
    df_godziny = {}
    df_kse_calosc = df_kse.reset_index()
    df_kse_calosc['Godzina'] = df_kse_calosc['Data'].dt.hour
    df_kse_calosc['Data'] = df_kse_calosc['Data'].dt.date
    df_kse_calosc = df_kse_calosc[nazwy_kolumn]
    for godzina in lista_godzin:
        df_godziny[godzina] = df_kse.loc[df_kse.index.hour == godzina]
        df_godziny[godzina] = df_godziny[godzina].reset_index()
        df_godziny[godzina]['Godzina'] = df_godziny[godzina]['Data'].dt.hour
        df_godziny[godzina]['Data'] = df_godziny[godzina]['Data'].dt.date
        df_godziny[godzina] = df_godziny[godzina][nazwy_kolumn]
    writer = pd.ExcelWriter(sciezka + '2009-2018' + nazwa_pliku_docelowego)
    df_kse_calosc.to_excel(writer, '2009-2018', index=False)
    print(f'Do listy arkuszy dodano: 2009-2018')
    for godzina, tabela in df_godziny.items():
        tabela.to_excel(writer, str(godzina), index=False)
        print(f'Do listy arkuszy dodano: {godzina}')
    writer.save()


def osobne_lata():
    lista_lat = list(df_kse.index.year.unique())
    lista_godzin = [godzina for godzina in range(24)]
    df_godziny = {}
    nazwa_pliku_docelowego = '_Typy_dni_KSE_Zestawienie.xlsx'
    for rok in lista_lat:
        df_godziny[rok] = {}
        df_godziny[rok][rok] = df_kse.loc[df_kse.index.year == rok]
        df_godziny[rok][rok] = df_godziny[rok][rok].reset_index()
        df_godziny[rok][rok]['Godzina'] = df_godziny[rok][rok]['Data'].dt.hour
        df_godziny[rok][rok]['Data'] = df_godziny[rok][rok]['Data'].dt.date
        df_godziny[rok][rok] = df_godziny[rok][rok][nazwy_kolumn]
        for godzina in lista_godzin:
            mask = (df_kse.index.year == rok) & (df_kse.index.hour == godzina)
            df_godziny[rok][godzina] = df_kse.loc[mask]
            df_godziny[rok][godzina] = df_godziny[rok][godzina].reset_index()
            df_godziny[rok][godzina]['Godzina'] = df_godziny[rok][godzina]['Data'].dt.hour
            df_godziny[rok][godzina]['Data'] = df_godziny[rok][godzina]['Data'].dt.date
            df_godziny[rok][godzina] = df_godziny[rok][godzina][nazwy_kolumn]
    for rok, tabele in df_godziny.items():
        writer = pd.ExcelWriter(sciezka + str(rok) + nazwa_pliku_docelowego)
        for nazwa_tabeli, tabela in tabele.items():
            tabela.to_excel(writer, str(nazwa_tabeli), index=False)
            print(f'Do listy arkuszy dodano: {nazwa_tabeli}')
        writer.save()


wszystkie_lata()

osobne_lata()
