import tkinter as tk
#from tkinter import Tk                                                  #remover futuramente (após testes)
import json

from time import sleep
from datetime import datetime
from tkinter import ttk
from coreslayout import *
from state_exec import estado_programa, estado_database

caminho_hist_crono = 'database_cronograma.json'
hora_atual = datetime.now()
hora_atual_form = hora_atual.strftime('%d/%m/%Y %H:%M:%S')

#janela_monitor = Tk()                                                  #remover futuramente (após testes)
class MonitorTarefas():
    def __init__(self):
     #   self.janela_monitor = janela_monitor                           #remover futuramente (após testes)
        self.janela_monitor = tk.Toplevel()
        self.janela_monitor.title('Monitor de execução')
        self.tela_ini_monit()
        self.frames_monitor()
     #   janela_monitor.mainloop()                                      #remover futuramente (após testes)

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

        self.frm_divisa1 = ttk.Frame(self.frm_fundo, relief='groove')
        self.frm_divisa1.place(relx=0.005, rely=0.06, relheight=0.0015, relwidth=0.77)

        self.lbl_passado = ttk.Label(self.frm_fundo, text='Iniciadas:', background=verde1, font=('Calibri bold', 13))
        self.lbl_passado.place(relx=0.006, rely=0.077)
        self.frm_passado = ttk.Frame(self.frm_fundo, relief='groove', style='')
        self.frm_passado.place(relx=0.006, rely=0.11, relheight=0.43, relwidth=0.77)


        self.lbl_futuro = ttk.Label(self.frm_fundo, text='Pendentes:', background=verde1, font=('Calibri bold', 13))
        self.lbl_futuro.place(relx=0.006, rely=0.567)
        self.frm_futuro = ttk.Frame(self.frm_fundo, relief='groove')
        self.frm_futuro.grid()
        self.frm_futuro.place(relx=0.006, rely=0.6, relheight=0.4, relwidth=0.77)


        self.frm_status_prg = ttk.Label(self.frm_fundo, relief='groove', background='', text=estado_programa, font=('Calibri bold', 18), justify='center')
        self.frm_status_prg.place(relx=0.798, rely=0.03, relheight=0.11, relwidth=0.18)
        self.atualiza_janela_monit()

    def atualiza_janela_monit(self):
        global itens_executados, itens_pendentes, hora_atual
        hora_atual = datetime.now()
        status_atual_prg = estado_programa.obtem_status()

        self.lbl_hora_atual = ttk.Label(self.frm_fundo, text=hora_atual_form, background=verde1, font=('Calibri bold', 15))
        self.lbl_hora_atual.place(relx=0.775, rely=0.005, anchor='ne')

        if status_atual_prg == 'Parado':
            self.frm_status_prg.config(text=status_atual_prg, background=vermelho0, foreground='white', font=('Calibri bold', 15), justify='center')
        else:
            self.frm_status_prg.config(text=status_atual_prg, background=verde_status, foreground='white', font=('Calibri bold', 15), justify='center')

        if estado_database.obtem_status_database() in ['Modificada', 'Inicio']:
            with open(caminho_hist_crono, 'r', encoding='utf-8') as arq_temp:
                itens_executados = []
                itens_pendentes = []
                crono_arq_conteudo = json.load(arq_temp)
                for x in crono_arq_conteudo:
                    if x['STATUS'] == 'Pendente':
                        itens_pendentes.append(x)
                    else:
                        itens_executados.append(x)
                print(itens_pendentes, '\n', itens_executados)
            estado_database.define_status_database('Não modificada')
        a = 0
        b = 0
        for col, labeL_item in enumerate(itens_executados):
            datax = labeL_item['ID'][:10]
            horas = labeL_item['HORA_INICIO'][:8]
            horario_validador = datetime.strptime(f"{datax} {horas}", '%d.%m.%Y %H:%M:%S')
            tempo_decorrido_bruto = 0
            if labeL_item['STATUS'] == 'Executando':
                tempo_decorrido_bruto = hora_atual - horario_validador
                total_segundos = int(tempo_decorrido_bruto.total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                tempo_decorrido_form = f'{horas:02}:{minutos:02}:{segundos:02}'

            print(f'\n{tempo_decorrido_form}')

            lab1 = ttk.Label(self.frm_passado, text=labeL_item['ATIVIDADE'], width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab2 = ttk.Label(self.frm_passado, text=labeL_item['HORA_INICIO'], width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab3 = ttk.Label(self.frm_passado, text=labeL_item['HORA_FIM'], width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab1.grid(row=a, column=b, padx=1, pady=1)
            lab2.grid(row=a, column=b+1, padx=1, pady=1)
            lab3.grid(row=a, column=b+2, padx=1, pady=1)
            a += 1

        self.janela_monitor.after(350, self.atualiza_janela_monit)
    




#MonitorTarefas()                                                       #remover futuramente (após testes)