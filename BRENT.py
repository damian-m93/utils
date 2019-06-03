import pandas as pd

tabela = pd.read_excel('C:/Users/ca125/Desktop/BRENT.xlsx')
tabela.set_index(tabela['Data'], inplace=True)
tabela.drop(columns=['Data'], inplace=True)
tabela.index = pd.MultiIndex.from_arrays([tabela.index.date, tabela.index.hour], names=['Data', 'Godzina'])

mask = tabela.loc[tabela['BRENT SPOT Price FOB [Dollars/Barrel]'].notnull()].index.get_level_values('Data')
tabela_wypelnione = tabela.loc[mask]['BRENT SPOT Price FOB [Dollars/Barrel]'].fillna(method='ffill')
tabela.update(tabela_wypelnione)

tabela.reset_index(inplace=True)

tabela.to_excel('C:/Users/ca125/Desktop/BRENT2.xlsx', index=False)

