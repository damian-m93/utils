import pandas as pd
import datetime as dt

df = pd.read_excel('C:/Users/ca125/Desktop/5tyg/Wyniki_zapotrzebowanie_KSE_prognozy+real.xlsx', index_col=0)

mask_III_prev5_2016 = (df.index >= dt.datetime(2016, 2, 21, 0, 0)) & (df.index <= dt.datetime(2016, 3, 26, 23, 59))
mask_III_prev5_2017 = (df.index >= dt.datetime(2017, 2, 19, 0, 0)) & (df.index <= dt.datetime(2017, 3, 25, 23, 59))
mask_III_prev5_2018 = (df.index >= dt.datetime(2018, 2, 18, 0, 0)) & (df.index <= dt.datetime(2018, 3, 24, 23, 59))

mask_III_next5_2016 = (df.index >= dt.datetime(2016, 3, 27, 0, 0)) & (df.index <= dt.datetime(2016, 4, 30, 23, 59))
mask_III_next5_2017 = (df.index >= dt.datetime(2017, 3, 26, 0, 0)) & (df.index <= dt.datetime(2017, 4, 29, 23, 59))
mask_III_next5_2018 = (df.index >= dt.datetime(2018, 3, 25, 0, 0)) & (df.index <= dt.datetime(2018, 4, 28, 23, 59))

mask_X_prev5_2016 = (df.index >= dt.datetime(2016, 9, 25, 0, 0)) & (df.index <= dt.datetime(2016, 10, 29, 23, 59))
mask_X_prev5_2017 = (df.index >= dt.datetime(2017, 9, 24, 0, 0)) & (df.index <= dt.datetime(2017, 10, 28, 23, 59))
mask_X_prev5_2018 = (df.index >= dt.datetime(2018, 9, 23, 0, 0)) & (df.index <= dt.datetime(2018, 10, 27, 23, 59))

mask_X_next5_2016 = (df.index >= dt.datetime(2016, 10, 30, 0, 0)) & (df.index <= dt.datetime(2016, 12, 3, 23, 59))
mask_X_next5_2017 = (df.index >= dt.datetime(2017, 10, 29, 0, 0)) & (df.index <= dt.datetime(2017, 12, 2, 23, 59))
mask_X_next5_2018 = (df.index >= dt.datetime(2018, 10, 28, 0, 0)) & (df.index <= dt.datetime(2018, 12, 1, 23, 59))

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

