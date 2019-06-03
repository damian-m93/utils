import pandas as pd
import xlsxwriter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option('expand_frame_repr', False)

sciezka = 'C:/Users/ca125/Desktop/Macierze/'
plik = sciezka + 'Zestawienie_zbiorcze.xlsx'
nazwa_pliku_docelowego = '_Macierze_korelacji.xlsx'


def macierze_rok():
    try:
        tabela_zbiorcza = pd.read_excel(plik, index_col=0)
        print(f'Pomyślnie wczytano plik: {plik}')
    except Exception as error:
        print(f'Błąd! Nie wczytano pliku: {plik}')
        print(error)

    lista_lat = list(tabela_zbiorcza.index.year.unique())
    lista_godzin = [godzina for godzina in range(24)]
    tabele_corr = {}
    lista_kolumn = list(tabela_zbiorcza.columns)
    lista_kolumn.remove('Wykonanie KSE')

    for rok in lista_lat:
        tabele_corr[rok] = {}
        tabele_corr[rok]['Zest_Wyk_KSE'] = pd.DataFrame(columns=lista_kolumn).append(
            tabela_zbiorcza.loc[tabela_zbiorcza.index.year == rok].corr().drop(
                columns=['Wykonanie KSE']).rename(index={'Wykonanie KSE': rok}).iloc[0])
        tabele_corr[rok][rok] = tabela_zbiorcza.loc[tabela_zbiorcza.index.year == rok].corr()
        for godzina in lista_godzin:
            mask = (tabela_zbiorcza.index.year == rok) & (tabela_zbiorcza.index.hour == godzina)
            tabele_corr[rok][godzina] = tabela_zbiorcza.loc[mask].corr()
            tabele_corr[rok]['Zest_Wyk_KSE'] = tabele_corr[rok]['Zest_Wyk_KSE'].append(
                tabele_corr[rok][godzina].drop(columns=['Wykonanie KSE']).rename(index={'Wykonanie KSE': godzina}).iloc[0])
        tabele_corr[rok]['Zest_Wyk_KSE'] = tabele_corr[rok]['Zest_Wyk_KSE'].append(
            tabele_corr[rok]['Zest_Wyk_KSE'].iloc[1:].mean(axis=0).rename('Średnia'))
        tabele_corr[rok]['Zest_Wyk_KSE'] = tabele_corr[rok]['Zest_Wyk_KSE'].append(
            tabele_corr[rok]['Zest_Wyk_KSE'].loc[rok].sub(
                tabele_corr[rok]['Zest_Wyk_KSE'].loc['Średnia']).rename('Różnica'))

    formatowanie_wiersze = [wiersz for wiersz in range(1,28)]
    for rok, tabele in tabele_corr.items():
        writer = pd.ExcelWriter(sciezka + str(rok) + nazwa_pliku_docelowego, engine='xlsxwriter')
        for nazwa_tabeli, tabela in tabele.items():
            tabela.to_excel(writer, str(nazwa_tabeli))
            print(f'Do listy arkuszy dodano: {nazwa_tabeli}')

        workbook = writer.book
        worksheet = writer.sheets['Zest_Wyk_KSE']
        format_liczby = workbook.add_format({'num_format': '0.000'})
        worksheet.set_column('B2:AJ28', 20, format_liczby)
        for wiersz in formatowanie_wiersze:
            worksheet.conditional_format(wiersz, 1, wiersz, 35, {'type': 'data_bar',
                                                                 'bar_color': '#63c384',
                                                                 'bar_solid': True,
                                                                 'bar_negative_color': '#ff0000'})
        writer.save()
        print(f'Zapisano plik: {rok}{nazwa_pliku_docelowego}')
    print(f'Pomyślnie wykonano wszystkie działania i zapisano pliki w: {sciezka}')


def macierze_agregacja():
    try:
        tabela_zbiorcza = pd.read_excel(plik, index_col=0)
        print(f'Pomyślnie wczytano plik: {plik}')
    except Exception as error:
        print(f'Błąd! Nie wczytano pliku: {plik}')
        print(error)

    lista_lat = list(tabela_zbiorcza.index.year.unique())
    lista_godzin = [godzina for godzina in range(24)]
    tabele_corr = {}
    lista_kolumn = list(tabela_zbiorcza.columns)
    lista_kolumn.remove('Wykonanie KSE')
    rok_do = lista_lat[-1]

    for rok in lista_lat:
        zakres_lat = str(rok) + '-' + str(rok_do)
        tabele_corr[zakres_lat] = {}
        tabele_corr[zakres_lat]['Zest_Wyk_KSE'] = pd.DataFrame(columns=lista_kolumn).append(
            tabela_zbiorcza.loc[str(rok):str(rok_do)].corr().drop(
                columns=['Wykonanie KSE']).rename(index={'Wykonanie KSE': zakres_lat}).iloc[0])
        tabele_corr[zakres_lat][zakres_lat] = tabela_zbiorcza.loc[str(rok):str(rok_do)].corr()
        for godzina in lista_godzin:
            tabela_zakres = tabela_zbiorcza.loc[str(rok):str(rok_do)]
            tabele_corr[zakres_lat][godzina] = tabela_zakres.loc[tabela_zakres.index.hour == godzina].corr()
            tabele_corr[zakres_lat]['Zest_Wyk_KSE'] = tabele_corr[zakres_lat]['Zest_Wyk_KSE'].append(
                tabele_corr[zakres_lat][godzina].drop(columns=['Wykonanie KSE']).rename(
                    index={'Wykonanie KSE': godzina}).iloc[0])
        tabele_corr[zakres_lat]['Zest_Wyk_KSE'] = tabele_corr[zakres_lat]['Zest_Wyk_KSE'].append(
            tabele_corr[zakres_lat]['Zest_Wyk_KSE'].iloc[1:].mean(axis=0).rename('Średnia'))
        tabele_corr[zakres_lat]['Zest_Wyk_KSE'] = tabele_corr[zakres_lat]['Zest_Wyk_KSE'].append(
            tabele_corr[zakres_lat]['Zest_Wyk_KSE'].loc[zakres_lat].sub(
                tabele_corr[zakres_lat]['Zest_Wyk_KSE'].loc['Średnia']).rename('Różnica'))

    formatowanie_wiersze = [wiersz for wiersz in range(1, 28)]
    for zakres, tabele in tabele_corr.items():
        writer = pd.ExcelWriter(sciezka + zakres + nazwa_pliku_docelowego, engine='xlsxwriter')
        for nazwa_tabeli, tabela in tabele.items():
            tabela.to_excel(writer, str(nazwa_tabeli))
            print(f'Do listy arkuszy dodano: {nazwa_tabeli}')

        workbook = writer.book
        worksheet = writer.sheets['Zest_Wyk_KSE']
        format_liczby = workbook.add_format({'num_format': '0.000'})
        worksheet.set_column('B2:AJ28', 20, format_liczby)
        for wiersz in formatowanie_wiersze:
            worksheet.conditional_format(wiersz, 1, wiersz, 35, {'type': 'data_bar',
                                                                 'bar_color': '#63c384',
                                                                 'bar_solid': True,
                                                                 'bar_negative_color': '#ff0000'})
        writer.save()
        print(f'Zapisano plik: {zakres}{nazwa_pliku_docelowego}')
    print(f'Pomyślnie wykonano wszystkie działania i zapisano pliki w: {sciezka}')


# macierze_rok()
macierze_agregacja()
