import pandas as pd
import datetime as dt

df = pd.read_excel('C:/Users/ca125/Desktop/okresy/Dane_wejściowe.xlsx', index_col=0)



zmiany_czasu_mar = {2009: dt.datetime(2009, 3, 29),
                    2010: dt.datetime(2010, 3, 28),
                    2011: dt.datetime(2011, 3, 27),
                    2012: dt.datetime(2012, 3, 25),
                    2013: dt.datetime(2013, 3, 31),
                    2014: dt.datetime(2014, 3, 30),
                    2015: dt.datetime(2015, 3, 29),
                    2016: dt.datetime(2016, 3, 27),
                    2017: dt.datetime(2017, 3, 26),
                    2018: dt.datetime(2018, 3, 25)}

zmiany_czasu_paz = {2009: dt.datetime(2009, 10, 25),
                    2010: dt.datetime(2010, 10, 31),
                    2011: dt.datetime(2011, 10, 30),
                    2012: dt.datetime(2012, 10, 28),
                    2013: dt.datetime(2013, 10, 27),
                    2014: dt.datetime(2014, 10, 26),
                    2015: dt.datetime(2015, 10, 25),
                    2016: dt.datetime(2016, 10, 30),
                    2017: dt.datetime(2017, 10, 29),
                    2018: dt.datetime(2018, 10, 28)}

lista_godzin_1 = [0, 12]
lista_godzin_2 = [5, 6, 7, 8, 17, 18, 19, 20, 21]

def stworz_start_koniec_prev(data_zmiany):
    prev_start = data_zmiany - dt.timedelta(days=7)
    prev_end = data_zmiany + dt.timedelta(days=1) - dt.timedelta(minutes=1)
    return prev_start, prev_end


def stworz_start_koniec_next(data_zmiany):
    next_start = data_zmiany
    next_end = data_zmiany + dt.timedelta(days=8) - dt.timedelta(minutes=1)
    return next_start, next_end


df_mar_prev = pd.DataFrame()
df_mar_next = pd.DataFrame()

for rok, data_zmiany in zmiany_czasu_mar.items():
    prev_start, prev_end = stworz_start_koniec_prev(data_zmiany)
    next_start, next_end = stworz_start_koniec_next(data_zmiany)
    mask_prev = (df.index >= prev_start) & (df.index <= prev_end)
    mask_next = (df.index >= next_start) & (df.index <= next_end)
#     df[mask_prev]
# df[df.index.hour.isin(lista_godzin_1)]
# df[df.index.hour.isin(lista_godzin_2)]




'''

df_III_prev5 = df[mask_III_prev5_2016].append(df[mask_III_prev5_2017].append(df[mask_III_prev5_2018]))
df_III_prev5_wyniki = df_III_prev5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
    df_III_prev5.index.year).max().join(
    df_III_prev5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
        df_III_prev5.index.year).sum(), lsuffix='_szczyt [MW]', rsuffix='_energia [MWh]').join(
    df_III_prev5.loc[:, 'Długość dnia':].groupby(df_III_prev5.index.year).mean())

df_III_next5 = df[mask_III_next5_2016].append(df[mask_III_next5_2017].append(df[mask_III_next5_2018]))
df_III_next5_wyniki = df_III_next5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
    df_III_next5.index.year).max().join(
    df_III_next5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
        df_III_next5.index.year).sum(), lsuffix='_szczyt [MW]', rsuffix='_energia [MWh]').join(
    df_III_next5.loc[:, 'Długość dnia':].groupby(df_III_next5.index.year).mean())

df_X_prev5 = df[mask_X_prev5_2016].append(df[mask_X_prev5_2017].append(df[mask_X_prev5_2018]))
df_X_prev5_wyniki = df_X_prev5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
    df_X_prev5.index.year).max().join(
    df_X_prev5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
        df_X_prev5.index.year).sum(), lsuffix='_szczyt [MW]', rsuffix='_energia [MWh]').join(
    df_X_prev5.loc[:, 'Długość dnia':].groupby(df_X_prev5.index.year).mean())

df_X_next5 = df[mask_X_next5_2016].append(df[mask_X_next5_2017].append(df[mask_X_next5_2018]))
df_X_next5_wyniki = df_X_next5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
    df_X_next5.index.year).max().join(
    df_X_next5.loc[:, :'Zapotrzebowanie - wartości rzeczywiste'].groupby(
        df_X_next5.index.year).sum(), lsuffix='_szczyt [MW]', rsuffix='_energia [MWh]').join(
    df_X_next5.loc[:, 'Długość dnia':].groupby(df_X_next5.index.year).mean())

df_III_prev5_wyniki.to_excel('C:/Users/ca125/Desktop/5tyg/Wyniki_marzec_-5.xlsx')
df_III_next5_wyniki.to_excel('C:/Users/ca125/Desktop/5tyg/Wyniki_marzec_+5.xlsx')
df_X_prev5_wyniki.to_excel('C:/Users/ca125/Desktop/5tyg/Wyniki_październik_-5.xlsx')
df_X_next5_wyniki.to_excel('C:/Users/ca125/Desktop/5tyg/Wyniki_październik_+5.xlsx')

'''

