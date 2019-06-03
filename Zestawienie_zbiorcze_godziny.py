import pandas as pd

df1 = pd.read_excel('C:/Users/ca125/Desktop/Zestawienie_zbiorcze_KSE_parametry.xlsx', index_col=0)
df2 = pd.read_excel('C:/Users/ca125/Desktop/Zestawienie_zbiorcze_KSE_rynek_gieldy.xlsx', index_col=0)

df2.index = df2.index + pd.to_timedelta(df2['Godzina'], unit='h')
col_list = list(df2.columns)

for col in col_list[2:]:
    df1 = df1.join(df2[col])

writer = pd.ExcelWriter('C:/Users/ca125/Desktop/Zestawienie_zbiorcze_godzinowe.xlsx')
df1.to_excel(writer, '0-23')
for godzina in range(0, 24):
    mask = (df1.index.hour == godzina)
    df1.loc[mask].to_excel(writer, str(godzina))
writer.save()



