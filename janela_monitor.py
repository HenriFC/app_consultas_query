import tkinter as Tk
from tkinter import PhotoImage
import json
from time import sleep

caminho_hist_crono = 'database_cronograma.json'


class monitor_tarefas():
    def __init__(self):
        self.caminho_hist_crono = caminho_hist_crono
        self.janela = Tk.Toplevel()
        self.janela.title("Monitor de Tarefas")
        #self.criar_widgets()
        img_ico2 = PhotoImage(file='icon1.png')
        self.janela.iconphoto(True, img_ico2)
