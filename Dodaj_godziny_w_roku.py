import pandas as pd

df = pd.read_excel('C:/Users/ca125/Desktop/KSE.xlsx', index_col=0)
lista_lat = list(df.index.year.unique())


for rok in lista_lat:
    godziny = [godzina for godzina in range(1, df.loc[str(rok)].index.size + 1)]
    df.loc[str(rok), 'Godzina w roku'] = godziny

lista_kolumn = ['Godzina w roku',
                'Dzień',
                'Typ dnia [R/W]',
                'Święto [S/NS/Wig]',
                'Zapotrzebowanie KSE [MW]',
                'Temperatura powietrza [°C]']

df = df[lista_kolumn]
df.to_excel('C:/Users/ca125/Desktop/Zmienność_obciążenia.xlsx')
