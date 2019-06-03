import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('expand_frame_repr', False)

sciezka_pliku = 'C:/Users/ca125/Desktop/Dane wejściowe.xlsx'

df = pd.read_excel(sciezka_pliku, index_col=0)

lista_lat = list(df.index.year.unique())
liczba_godz_rok = {}  # Liczba godzin w danym roku
energia_rok = {}  # Sumaryczne zapotrzebowanie w ciągu danego roku
moc_szczyt_rok = {}  # Wartość mocy szczytowej w danym roku
sr_moc_rok = {}  # Średnie godzinowe zapotrzebowanie na moc w ciągu danego roku
wzgl_przyr_en_rok = {}  # Względny przyrost energii w danym roku
wzgl_przyr_moc_szczyt_rok = {}  # Względny przyrost mocy szczytowej w danym roku
sr_stat_moc_rok = {}  # Wartość średnia statycznego zapotrzebowania w danym roku


def energia_w_roku(rok):
    return df.groupby(by=df.index.year).sum().loc[rok, 'Zapotrzebowanie KSE [MW]']


def moc_szczytowa_w_roku(rok):
    return df.groupby(by=df.index.year).max().loc[rok, 'Zapotrzebowanie KSE [MW]']


def sr_moc_w_roku(rok):
    return df.groupby(by=df.index.year).mean().loc[rok, 'Zapotrzebowanie KSE [MW]']


def wzgl_przyr_en_w_roku(rok):
    """ Dobrzańska, 2002, str. 20, współczynnik alfa Ar """
    rok_poprzedni = rok - 1
    return (energia_rok[rok] / energia_rok[rok_poprzedni]) - 1


def wzgl_przyr_moc_szczyt_w_roku(rok):
    rok_poprzedni = rok - 1
    return (moc_szczyt_rok[rok] / moc_szczyt_rok[rok_poprzedni]) - 1


def sr_stat_moc_w_roku(rok):
    return sr_moc_rok[rok] / (1 + (wzgl_przyr_en_rok[rok] / 2))


def stat_moc_w_godz(row):
    rok = row.name.year
    godzina = row['Godzina w roku']
    moc_godz = row['Zapotrzebowanie KSE [MW]']
    return (1 / (1 + ((godzina / liczba_godz_rok[rok]) *
                      ((wzgl_przyr_en_rok[rok] + wzgl_przyr_moc_szczyt_rok[rok]) / 2)))) * moc_godz


def stat_st_obc(row):
    rok = row.name.year
    return sr_stat_moc_rok[rok] / row['Wartość statyczna mocy']


def moc_normatywna(row):
    rok = row.name.year
    return sr_moc_rok[rok] / row['Statyczny stopień obciążenia']


for rok in lista_lat:
    liczba_godz_rok[rok] = df.loc[str(rok)].index.size
    energia_rok[rok] = energia_w_roku(rok)
    moc_szczyt_rok[rok] = moc_szczytowa_w_roku(rok)
    sr_moc_rok[rok] = sr_moc_w_roku(rok)


for rok in lista_lat[1:]:
    wzgl_przyr_en_rok[rok] = wzgl_przyr_en_w_roku(rok)
    wzgl_przyr_moc_szczyt_rok[rok] = wzgl_przyr_moc_szczyt_w_roku(rok)
    sr_stat_moc_rok[rok] = sr_stat_moc_w_roku(rok)

# Dodaj kolumnę z wartościami statycznego zapotrzebowania w danej godzinie (Ph stat)

df['Wartość statyczna mocy'] = df.loc['2010':].apply(stat_moc_w_godz, axis=1)

# Dodaj kolumnę z wartościami statycznego stopnia obciążenia w danej godzinie (mh stat)

df['Statyczny stopień obciążenia'] = df.loc['2010':].apply(stat_st_obc, axis=1)

# Dodaj kolumnę z wartościami normatywnego zapotrzebowania w danej godzinie (Ph)

df['Normatywne zapotrzebowanie'] = df.loc['2010':].apply(moc_normatywna, axis=1)

print(df)

df.to_excel('C:/Users/ca125/Desktop/test1.xlsx')




