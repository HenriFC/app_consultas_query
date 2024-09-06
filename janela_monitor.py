import tkinter as tk
import json

from time import sleep
from datetime import datetime, timedelta
from tkinter import ttk
from coreslayout import *
from state_exec import estado_programa, estado_database

caminho_hist_crono = 'database_cronograma.json'
global hora_atual
hora_atual = datetime.now()
hora_atual_exib_relog = hora_atual.strftime('%d/%m/%Y %H:%M:%S')


class MonitorTarefas():
    def __init__(self):
     #   self.janela_monitor = janela_monitor                           #remover futuramente (após testes)
        self.janela_monitor = tk.Toplevel()
        self.janela_monitor.title('Monitor de execução')
        self.labels_executados = []
        self.labels_pendentes = []
        self.tela_ini_monit()
        self.frames_monitor()
        self.atualiza_janela_monit()
        self.atualiza_relogio_monit()
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
        self.lbl_hora_atual_exib = ttk.Label(self.frm_fundo, text=hora_atual_exib_relog, background=verde1, font=('Calibri bold', 15))
        self.lbl_hora_atual_exib.place(relx=0.775, rely=0.005, anchor='ne')

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


        self.frm_status_prg = ttk.Label(self.frm_fundo, anchor='center', relief='groove', background='', text=estado_programa, font=('Calibri bold', 18), justify='center')
        self.frm_status_prg.place(relx=0.798, rely=0.03, relheight=0.11, relwidth=0.18)


    def atualiza_relogio_monit(self):
        hora_atual_exib = hora_atual.strftime('%d/%m/%Y %H:%M:%S')
        self.lbl_hora_atual_exib.config(text=hora_atual_exib)
        self.janela_monitor.after(50, self.atualiza_relogio_monit)

    def atualiza_janela_monit(self):
        global itens_executados, itens_pendentes, hora_atual
        hora_atual = datetime.now()
        status_atual_prg = estado_programa.obtem_status()

        if status_atual_prg in('Parado', 'Inicio'):
            self.frm_status_prg.config(text='Parado', background=vermelho0, foreground='white', font=('Calibri bold', 15), justify='center')
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
            estado_database.define_status_database('Não modificada')

        self.atualiza_labels(itens_executados, self.labels_executados, self.frm_passado)

        # Atualizar as labels para os itens pendentes
        self.atualiza_labels(itens_pendentes, self.labels_pendentes, self.frm_futuro)

        # Chamar a função novamente após 200ms
        self.janela_monitor.after(1000, self.atualiza_janela_monit)

    def atualiza_labels(self, itens, labels_lista, frame):
        # Se necessário, cria os widgets uma vez
        while len(labels_lista) < len(itens):
            lab0 = ttk.Label(frame, width=5, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab1 = ttk.Label(frame, width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab2 = ttk.Label(frame, width=7, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab3 = ttk.Label(frame, width=7, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab4 = ttk.Label(frame, width=7, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab5 = ttk.Label(frame, width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab6 = ttk.Label(frame, width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            lab7 = ttk.Label(frame, width=23, anchor='w', font=('Calibri', 10), justify='left', background=verde1)
            labels_lista.append((lab0, lab1, lab2, lab3, lab4,lab5, lab6, lab7))

        # Atualiza o texto dos widgets existentes
        for i, label_item in enumerate(itens):
            tempo_decorrido = label_item['TEMPO_EXEC']
            if label_item['STATUS'] == 'Executando':
                tempo_decorrido_str = f"{label_item['ID'][6:10]}-{label_item['ID'][3:5]}-{label_item['ID'][:2]} {label_item['HORA_INICIO']}"
                tempo_decorrido = hora_atual - datetime.strptime(tempo_decorrido_str, '%Y-%m-%d %H:%M:%S')
                total_segundos = int(tempo_decorrido.total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                tempo_decorrido = f'{horas:02}:{minutos:02}:{segundos:02}'

            if i < len(labels_lista):
                lab0, lab1, lab2, lab3, lab4, lab5, lab6, lab7 = labels_lista[i]
                lab0.config(text='Icon')
                lab1.config(text=label_item['ATIVIDADE'])
                lab2.config(text=label_item['HORA_INICIO'])
                lab3.config(text=label_item['HORA_FIM'])
                lab4.config(text=tempo_decorrido)
                lab5.config(text=label_item['NOME_ARQUIVO'])

                lab0.grid(row=i, column=0, padx=2, pady=2)
                lab1.grid(row=i, column=1, padx=2, pady=2)
                lab2.grid(row=i, column=2, padx=2, pady=2)
                lab3.grid(row=i, column=3, padx=2, pady=2)
                lab4.grid(row=i, column=4, padx=2, pady=2)