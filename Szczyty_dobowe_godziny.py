import pandas as pd

pliki = ['C:/Users/ca125/Desktop/Obciążenia_przesunięcia_marzec.xlsx',
         'C:/Users/ca125/Desktop/Obciążenia_przesunięcia_październik.xlsx']
sciezka_docelowa = 'C:/Users/ca125/Desktop/'
col_P = 'Zapotrzebowanie KSE [MW]'

for plik in pliki:
    nazwa_pliku = plik.split('/')[-1].split('.')[0] + '_szczyty.xlsx'
    writer = pd.ExcelWriter(sciezka_docelowa + nazwa_pliku)
    df_wszystkie = pd.read_excel(plik, sheet_name=None, index_col=0)
    for nazwa, df in df_wszystkie.items():
        tabela = pd.DataFrame()
        tabela['Pmax'] = df.groupby(by=df.index.date)[col_P].max()
        tabela['Godzina Pmax'] = df.groupby(by=df.index.date)[col_P].idxmax()
        mask1 = df.index.hour <= 11
        tabela['Pmax 0-11'] = df.loc[mask1].groupby(by=df.loc[mask1].index.date)[col_P].max()
        tabela['Godzina Pmax 0-11'] = df.loc[mask1].groupby(by=df.loc[mask1].index.date)[col_P].idxmax()
        mask2 = df.index.hour >= 12
        tabela['Pmax 12-23'] = df.loc[mask2].groupby(by=df.loc[mask2].index.date)[col_P].max()
        tabela['Godzina Pmax 12-23'] = df.loc[mask2].groupby(by=df.loc[mask2].index.date)[col_P].idxmax()
        tabela.to_excel(writer, nazwa)
    writer.save()


