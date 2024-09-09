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
        self.janela_monitor = tk.Toplevel()
        self.janela_monitor.title('Monitor de execução')
        self.labels_finalizados = []
        self.labels_executando = []
        self.labels_pendentes = []
        self.labels_titulos = ['Icon', 'Query', 'Inicio', 'Fim', 'Tempo', 'Status', 'Observação']
        self.tela_ini_monit()
        self.frames_monitor()
        self.atualiza_janela_monit()
        self.atualiza_relogio_monit()

    def tela_ini_monit(self):

        larg_tela = self.janela_monitor.winfo_screenwidth()
        altu_tela = self.janela_monitor.winfo_screenheight()
        self.janela_monitor.config(bg=verde4)
        self.janela_monitor.geometry('1300x600+50+77')
        self.janela_monitor.minsize(width='1300', height='600')
        self.janela_monitor.maxsize(width=larg_tela, height=altu_tela)


    def frames_monitor(self):
        self.frm_fundo = ttk.Frame(self.janela_monitor, style='frm_back.TFrame')
        self.frm_fundo.place(relx=0.006, rely=0.01, relheight=0.98, relwidth=0.988)
        self.lbl_titulo = ttk.Label(self.frm_fundo, text='Monitor de Tarefas', background=verde1, font=('Calibri bold', 17))
        self.lbl_titulo.place(relx=0.005, rely=0.005)
        self.lbl_hora_atual_exib = ttk.Label(self.frm_fundo, text=hora_atual_exib_relog, background=verde1, font=('Calibri bold', 15))
        self.lbl_hora_atual_exib.place(relx=0.775, rely=0.005, anchor='ne')
        self.frm_status_prg = ttk.Label(self.frm_fundo, anchor='center', relief='groove', background='', text=estado_programa, font=('Calibri bold', 18), justify='center')
        self.frm_status_prg.place(relx=0.81, rely=0.03, relheight=0.08, relwidth=0.18)

        self.lbl_passado = ttk.Label(self.frm_fundo, text='Iniciadas:', background=verde1, font=('Calibri bold', 13))
        self.lbl_passado.place(relx=0.006, rely=0.077)
        self.lbl_futuro = ttk.Label(self.frm_fundo, text='Pendentes:', background=verde1, font=('Calibri bold', 13))
        self.lbl_futuro.place(relx=0.006, rely=0.64)
        self.frm_divisa1 = ttk.Frame(self.frm_fundo, relief='groove')
        self.frm_divisa1.place(relx=0.005, rely=0.06, relheight=0.0015, relwidth=0.77)
        self.frm_passado_back = ttk.Frame(self.frm_fundo, relief='groove', style='frm_pass.TFrame', padding=2)
        self.frm_passado_back.place(relx=0.006, rely=0.11, relheight=0.5)
        self.frm_futuro_back = ttk.Frame(self.frm_fundo, relief='groove', style='frm_pass.TFrame', padding=2)
        self.frm_futuro_back.place(relx=0.006, rely=0.673, relheight=0.29)

  #  #  #  #  #  #  #  #  #  #

        self.frm_passado_finalizadas = ttk.Frame(self.frm_passado_back, relief='groove')
        self.frm_passado_finalizadas.place(relx=0.001, rely=0.065, relheight=0.46, relwidth=0.998)
        self.canva_passado_finaliz = tk.Canvas(self.frm_passado_finalizadas, borderwidth=0, relief='groove')
        self.scroll_passado_finaliz = ttk.Scrollbar(self.frm_passado_finalizadas, cursor='arrow', orient='vertical', command=self.canva_passado_finaliz.yview)
        self.frm_passado_finaliz_scr = ttk.Frame(self.canva_passado_finaliz)

        self.canva_passado_finaliz.bind('<Configure>', lambda e: self.canva_passado_finaliz.configure(scrollregion=self.canva_passado_finaliz.bbox('all')))
        self.canva_passado_finaliz.create_window((0, 0), window=self.frm_passado_finaliz_scr, anchor='nw')
        self.canva_passado_finaliz.configure(yscrollcommand=self.scroll_passado_finaliz.set, bg='white')
        self.canva_passado_finaliz.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        self.scroll_passado_finaliz.place(anchor='ne', relx=0.998, rely=0.005, relheight=0.98)

        self.canva_passado_finaliz.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.frm_passado_finaliz_scr.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.frm_passado_execut = ttk.Frame(self.frm_passado_back, relief='groove')
        self.frm_passado_execut.place(relx=0.001, rely=0.54, relheight=0.46, relwidth=0.998)

        self.canva_passado_execut = tk.Canvas(self.frm_passado_execut, borderwidth=0, relief='groove')
        self.scroll_passado_execut = ttk.Scrollbar(self.frm_passado_execut, cursor='arrow', orient='vertical', command=self.canva_passado_execut.yview)
        self.frm_passado_execut_scr = ttk.Frame(self.canva_passado_execut)

        self.canva_passado_execut.bind('<Configure>', lambda e: self.canva_passado_execut.configure(scrollregion=self.canva_passado_execut.bbox('all')))
        self.canva_passado_execut.create_window((0, 0), window=self.frm_passado_execut_scr, anchor='nw')
        self.canva_passado_execut.configure(yscrollcommand=self.scroll_passado_execut.set, bg='white')
        self.canva_passado_execut.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        self.scroll_passado_execut.place(anchor='ne', relx=0.998, rely=0.005, relheight=0.98)

        self.canva_passado_execut.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.frm_passado_execut_scr.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.frm_futuro_pend = ttk.Frame(self.frm_futuro_back, relief='groove')
        self.frm_futuro_pend.place(relx=0.001, rely=0.112, relheight=0.89, relwidth=0.998)

        self.canva_futuro = tk.Canvas(self.frm_futuro_pend, borderwidth=0, relief='groove')
        self.scroll_futuro = ttk.Scrollbar(self.frm_futuro_pend, cursor='arrow', orient='vertical', command=self.canva_futuro.yview)
        self.frm_futuro_scr = ttk.Frame(self.canva_futuro)

        self.frm_futuro_scr.bind('<Configure>', lambda e: self.canva_futuro.configure(scrollregion=self.canva_futuro.bbox('all')))
        self.canva_futuro.create_window((0, 0), window=self.frm_futuro_scr, anchor='nw')
        self.canva_futuro.configure(yscrollcommand=self.scroll_futuro.set, bg='white')
        self.canva_futuro.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        self.scroll_futuro.place(anchor='ne', relx=0.998, rely=0.005, relheight=0.98)

        # Evento para scroll by wheel
        self.canva_futuro.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.frm_futuro_scr.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.insere_titulo(self.frm_passado_back)
        self.insere_titulo(self.frm_futuro_back)

    def _on_mouse_wheel(self, event):
        """
        Define o comportamento do scroll com a roda do mouse.
        """
        widget_containing = self.janela_monitor.winfo_containing(event.x_root, event.y_root)

        if widget_containing == self.canva_passado_finaliz or widget_containing in self.frm_passado_finaliz_scr.winfo_children():
            self.canva_passado_finaliz.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif widget_containing == self.canva_passado_execut or widget_containing in self.frm_passado_execut_scr.winfo_children():
            self.canva_passado_execut.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif widget_containing == self.canva_futuro or widget_containing in self.frm_futuro_scr.winfo_children():
            self.canva_futuro.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def atualiza_relogio_monit(self):
        hora_atual_exib = hora_atual.strftime('%d/%m/%Y %H:%M:%S')
        self.lbl_hora_atual_exib.config(text=hora_atual_exib)
        self.janela_monitor.after(50, self.atualiza_relogio_monit)

    def atualiza_janela_monit(self):
        global itens_finalizados, itens_executando, itens_pendentes, hora_atual
        hora_atual = datetime.now()
        status_atual_prg = estado_programa.obtem_status()

        if status_atual_prg in('Parado', 'Inicio'):
            self.frm_status_prg.config(text='Parado', background=vermelho0, foreground='white', font=('Calibri bold', 15), justify='center')
        else:
            self.frm_status_prg.config(text=status_atual_prg, background=verde_status, foreground='white', font=('Calibri bold', 15), justify='center')

        if estado_database.obtem_status_database() in ['Modificada', 'Inicio']:
            with open(caminho_hist_crono, 'r', encoding='utf-8') as arq_temp:
                itens_finalizados = []
                itens_executando = []
                itens_pendentes = []
                crono_arq_conteudo = json.load(arq_temp)
                for x in crono_arq_conteudo:
                    if x['STATUS'] == 'Pendente':
                        itens_pendentes.append(x)
                    elif x['STATUS'] == 'Executando':
                        itens_executando.append(x)
                    else:
                        itens_finalizados.append(x)
                estado_database.define_status_database('Não modificada')
                itens_finalizados = sorted(sorted(itens_finalizados, key=lambda reg: reg['HORA_FIM_CONS'], reverse=True), key=lambda reg: reg['DATA'], reverse=True)
                itens_executando = sorted(sorted(itens_executando, key=lambda reg: reg['HORA_FIM_CONS'], reverse=True), key=lambda reg: reg['DATA'], reverse=True)
                itens_pendentes = sorted(sorted(itens_pendentes, key=lambda reg: reg['HORA_INICIO_PLAN']), key=lambda reg: reg['DATA'])

        
        self.atualiza_labels(itens_finalizados, self.labels_finalizados, self.frm_passado_finaliz_scr)

        self.atualiza_labels(itens_executando, self.labels_executando, self.frm_passado_execut_scr)

        self.atualiza_labels(itens_pendentes, self.labels_pendentes, self.frm_futuro_scr)

        self.janela_monitor.after(1000, self.atualiza_janela_monit)

    def insere_titulo(self, frame):
        
        lab0 = ttk.Label(frame, width=4, anchor='cente', font=('Calibri', 9), justify='center', background=light_cian)
        lab1 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab2 = ttk.Label(frame, width=25, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab3 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab4 = ttk.Label(frame, width=14, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab5 = ttk.Label(frame, width=12, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab6 = ttk.Label(frame, width=14, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab7 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab8 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab9 = ttk.Label(frame, width=19, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)
        lab10 = ttk.Label(frame, width=21, anchor='center', font=('Calibri', 9), justify='center', background=light_cian)

        lab0.config(text='*', border=10)
        lab1.config(text='Status')
        lab2.config(text='Atividade')
        lab3.config(text='Data')
        lab4.config(text='Inicio plan.')
        lab5.config(text='Inicio real')
        lab6.config(text='Atraso')
        lab7.config(text='Fim')
        lab8.config(text='Tempo')
        lab9.config(text='Nome do arquivo')
        lab10.config(text='OBSERVAÇÃO')

        lab0.grid(row=0, column=0, padx=1, pady=1)
        lab1.grid(row=0, column=1, padx=0, pady=1)
        lab2.grid(row=0, column=2, padx=0, pady=1)
        lab3.grid(row=0, column=3, padx=0, pady=1)
        lab4.grid(row=0, column=4, padx=0, pady=1)
        lab5.grid(row=0, column=5, padx=0, pady=1)
        lab6.grid(row=0, column=6, padx=0, pady=1)
        lab7.grid(row=0, column=7, padx=0, pady=1)
        lab8.grid(row=0, column=8, padx=0, pady=1)
        lab9.grid(row=0, column=9, padx=0, pady=1)
        lab10.grid(row=0, column=10, padx=0, pady=1)

    def atualiza_labels(self, itens, labels_lista, frame):

        if len(labels_lista) > len(itens):
            for label_set in labels_lista[len(itens):]:
                for label in label_set:
                    label.destroy()
            del labels_lista[len(itens):]


        while len(labels_lista) < len(itens):
            lab0 = ttk.Label(frame, width=4, anchor='center', font=('Calibri', 9), justify='center')
            lab1 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab2 = ttk.Label(frame, width=25, anchor='center', font=('Calibri', 9), justify='center')
            lab3 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab4 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab5 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab6 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab7 = ttk.Label(frame, width=14, anchor='center', font=('Calibri', 9), justify='center')
            lab8 = ttk.Label(frame, width=13, anchor='center', font=('Calibri', 9), justify='center')
            lab9 = ttk.Label(frame, width=19, anchor='center', font=('Calibri', 9), justify='center')
            lab10 = ttk.Label(frame, width=21, anchor='center', font=('Calibri', 9), justify='center')
            labels_lista.append((lab0, lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9, lab10))

            lab0.grid(row=len(labels_lista) - 1, column=0, padx=2, pady=1)
            lab1.grid(row=len(labels_lista) - 1, column=1, padx=2, pady=1)
            lab2.grid(row=len(labels_lista) - 1, column=2, padx=2, pady=1)
            lab3.grid(row=len(labels_lista) - 1, column=3, padx=2, pady=1)
            lab4.grid(row=len(labels_lista) - 1, column=4, padx=2, pady=1)
            lab5.grid(row=len(labels_lista) - 1, column=5, padx=2, pady=1)
            lab6.grid(row=len(labels_lista) - 1, column=6, padx=2, pady=1)
            lab7.grid(row=len(labels_lista) - 1, column=7, padx=2, pady=1)
            lab8.grid(row=len(labels_lista) - 1, column=8, padx=2, pady=1)
            lab9.grid(row=len(labels_lista) - 1, column=9, padx=2, pady=1)
            lab10.grid(row=len(labels_lista) - 1, column=10, padx=2, pady=1)

        list_par = stat_cor1

        for i, item in enumerate(itens):
            tempo_decorrido = item['TEMPO_EXEC']

            if item['STATUS'] == 'Executando':
                tempo_decorrido_str = f"{item['ID'][6:10]}-{item['ID'][3:5]}-{item['ID'][:2]} {item['HORA_INICIO_CONS']}"
                tempo_decorrido = hora_atual - datetime.strptime(tempo_decorrido_str, '%Y-%m-%d %H:%M:%S')
                total_segundos = int(tempo_decorrido.total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                tempo_decorrido = f'{horas:02}:{minutos:02}:{segundos:02}'

            lab0, lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9, lab10 = labels_lista[i]

            if i % 2 == 0:
                list_par = stat_cor1


            lab0.config(text='Icon', background=list_par)
            lab1.config(text=item['STATUS'], background=list_par)
            lab2.config(text=item['ATIVIDADE'], background=list_par)
            lab3.config(text=item['DATA'], background=list_par)
            lab4.config(text=item['HORA_INICIO_PLAN'], background=list_par)
            lab5.config(text=item['HORA_INICIO_CONS'], background=list_par)
            lab6.config(text=item['ATRASO'], background=list_par)
            lab7.config(text=item['HORA_FIM_CONS'], background=list_par)
            lab8.config(text=tempo_decorrido, background=list_par)
            lab9.config(text=item['NOME_ARQUIVO'], background=list_par)
            lab10.config(text=item['OBSERVAÇÃO'], background=list_par)


            lab0.grid(row=i, column=0, padx=0, pady=0)
            lab1.grid(row=i, column=1, padx=0, pady=0)
            lab2.grid(row=i, column=2, padx=0, pady=0)
            lab3.grid(row=i, column=3, padx=0, pady=0)
            lab4.grid(row=i, column=4, padx=0, pady=0)
            lab5.grid(row=i, column=5, padx=0, pady=0)
            lab6.grid(row=i, column=6, padx=0, pady=0)
            lab7.grid(row=i, column=7, padx=0, pady=0)
            lab8.grid(row=i, column=8, padx=0, pady=0)
            lab9.grid(row=i, column=9, padx=0, pady=0)
            lab10.grid(row=i, column=10, padx=0, pady=0)
            list_par = stat_cor2

                