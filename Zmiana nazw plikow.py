import os

katalog = 'C:/Users/Damian/Desktop/PlikiDoZmiany/'
numer = 216

for plik in os.listdir(katalog):
    nazwa_pliku_old = katalog + plik
    nazwa_pliku_new = katalog + 'C' + str(numer) + '.pdf'
    os.rename(nazwa_pliku_old, nazwa_pliku_new)
    numer += 1

