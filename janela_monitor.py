import tkinter as tk
#from tkinter import Tk                                                  #remover futuramente (após testes)
import json

from time import sleep
from datetime import datetime
from tkinter import ttk
from coreslayout import *
from state_exec import estado_programa

caminho_hist_crono = 'database_cronograma.json'
hora_atual = datetime.now()
hora_atual_form = hora_atual.strftime('%d/%m/%Y %H:%M')

#janela_monitor = Tk()                                                  #remover futuramente (após testes)
class MonitorTarefas():
    def __init__(self):
 #       self.janela_monitor = janela_monitor                           #remover futuramente (após testes)
        self.janela_monitor = tk.Toplevel()
        self.janela_monitor.title('Monitor de execução')
        self.tela_ini_monit()
        self.frames_monitor()

  #      janela_monitor.mainloop()                                      #remover futuramente (após testes)


    def tela_ini_monit(self):

        larg_tela = self.janela_monitor.winfo_screenwidth()
        altu_tela = self.janela_monitor.winfo_screenheight()
        self.janela_monitor.config(bg=verde4)
        self.janela_monitor.geometry('1100x600+77+77')
        self.janela_monitor.minsize(width='800', height='600')
        self.janela_monitor.maxsize(width=larg_tela, height=altu_tela)


    def frames_monitor(self):
        self.frm_fundo = ttk.Frame(self.janela_monitor, style='frm_back.TFrame')
        self.frm_fundo.place(relx=0.006, rely=0.01, relheight=0.98, relwidth=0.988)
        self.lbl_titulo = ttk.Label(self.frm_fundo, text='Monitor de Tarefas', background=verde1, font=('Calibri bold', 17))
        self.lbl_titulo.place(relx=0.005, rely=0.005)
        self.lbl_hora_atual = ttk.Label(self.frm_fundo, text=hora_atual_form, background=verde1, font=('Calibri bold', 15))
        self.lbl_hora_atual.place(relx=0.775, rely=0.005, anchor='ne')

        self.frm_divisa1 = ttk.Frame(self.frm_fundo, relief='groove')
        self.frm_divisa1.place(relx=0.005, rely=0.07, relheight=0.0015, relwidth=0.77)

        self.frm_passado = ttk.Frame(self.frm_fundo, relief='groove', style='')
        self.frm_passado.place(relx=0.006, rely=0.1, relheight=0.3, relwidth=0.77)

        self.frm_futuro = ttk.Frame(self.frm_fundo, relief='groove')
        self.frm_futuro.place(relx=0.006, rely=0.6, relheight=0.4, relwidth=0.77)

        self.frm_status_prg = ttk.Label(self.frm_fundo, relief='groove', background='', text=estado_programa, font=('Calibri bold', 12))
        self.frm_status_prg.place(relx=0.798, rely=0.03, relheight=0.11, relwidth=0.18)
        self.atualizar_tudo()

    def atualizar_tudo(self):
        status_atual_prg = estado_programa.obtem_status()
        self.frm_status_prg.config(text=status_atual_prg)
        self.janela_monitor.after(500, self.atualizar_tudo)


    


#monitor_tarefas()                                                       #remover futuramente (após testes)