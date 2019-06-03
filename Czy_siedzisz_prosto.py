from tkinter import *
import random
import time

while True:
    czas = random.randrange(0, 3601)
    time.sleep(czas)
    okno = Tk()
    okno.geometry("950x120")
    okno.title("Przypomnienie!")
    tekst = Text(okno, height=120, width=950)
    tekst.tag_configure('wzor', font=('Arial', 70, 'bold', 'italic'))
    tekst.insert(END, 'Czy siedzisz prosto?', 'wzor')
    tekst.pack()
    okno.mainloop()

