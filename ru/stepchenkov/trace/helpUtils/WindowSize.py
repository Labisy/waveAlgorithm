from tkinter import Tk, Label, Button, Entry
from ru.stepchenkov.trace import Main


def clicked():
    Main.start()


window = Tk()
window.title("Установка размеров")
window.geometry('400x250')

lbl = Label(window, text="W")
lbl.grid(column=0, row=0)
lbl2 = Label(window, text="H")
lbl2.grid(column=0, row=1)

weight = Entry(window, width=10)
weight.grid(column=1, row=0)

height = Entry(window, width=10)
height.grid(column=1, row=1)

btn = Button(window, text="Запуск сетки", command=clicked)
btn.grid(column=0, row=12)
window.mainloop()
