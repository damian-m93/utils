import pandas as pd


def dlugosc_dnia():
    df = pd.read_excel('C:/Users/ca125/Desktop/Dane_wejściowe_test.xlsx', index_col=0)
    df2 = pd.read_excel('C:/Users/ca125/Desktop/Długość dnia.xlsx', sheet_name='Warszawa (wszystkie lata)', index_col=0)
    df2['Długość dnia'] = pd.to_datetime(df2['Długość dnia'], format='%Hg %Mm')
    df2['Długość dnia'] = df2['Długość dnia'].apply(lambda row: (row.hour * 60) + row.minute)
    df = df.join(df2['Długość dnia'])
    df['Długość dnia'].fillna(method='ffill', inplace=True)
    df.to_excel('C:/Users/ca125/Desktop/Dane_wejściowe.xlsx')


def wschody_zachody():
    df = pd.read_excel('C:/Users/ca125/Desktop/Dane_wejściowe_test.xlsx', index_col=0)
    df2 = pd.read_excel('C:/Users/ca125/Desktop/Wschody-Zachody-Dł.dnia_DM.xlsx', index_col=0)
    df2['Wschód słońca'] = df2['Wschód słońca'].apply(lambda row: (row.hour * 60) + row.minute)
    df2['Zachód słońca'] = df2['Zachód słońca'].apply(lambda row: (row.hour * 60) + row.minute)
    df = df.join(df2['Wschód słońca'])
    df = df.join(df2['Zachód słońca'])
    df['Wschód słońca'].fillna(method='ffill', inplace=True)
    df['Zachód słońca'].fillna(method='ffill', inplace=True)
    df.to_excel('C:/Users/ca125/Desktop/Dane_wejściowe.xlsx')


wschody_zachody()
