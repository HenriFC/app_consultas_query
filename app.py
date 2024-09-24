import os
import json
import shutil
import tempfile
from tkinter import Tk, PhotoImage, Scrollbar, Text, Toplevel
from tkinter import ttk
from tkinter import messagebox

from autoedge import iniciar_edge
from cronograma_geral import obter_cronograma_status
from janela_monitor import MonitorTarefas
from state_exec import estado_programa, estado_database
from coreslayout import *
from iniciar_exec import click_start_stop, obter_email


jan_principal = Tk()
img_ico = PhotoImage(file='icon2.png')
jan_principal.iconphoto(True, img_ico)
s = ttk.Style()
s.map('TButton', background=[('active', azul_claro), ('disabled', 'light grey')], foreground=[('active', 'blue'), ('disabled', 'grey')])
s.configure('frm_status_start.TFrame', background=verde0)
s.configure('frm_status_stop.TFrame', background=vermelho0)
s.configure('frm_back.TFrame', background=verde1)
s.configure('frm_pass.TFrame', background=light_cian)

CAMINHO_DB_JSON = 'database.json'
CAMINHO_HIST_CRONO = 'database_cronograma.json'
CAMINHO_DB_EMAIL = 'database_email.json'

global nome_antigo_query




class ValidarEntrys():

    def validar_entry_nome(self, text):
        if len(text) <= 27:
            return True
        return False

    def validar_entry_horario(self, text):
        if text == '': 
            return True

        try:
            if len(text) > 5:
                return False
            
            if len(text) == 1 and int(text[0]) >= 3:
                return False

            if len(text) == 2 and int(text[0:2]) >= 24:
                return False

            if len(text) == 3 and text[2] != ':':
                return False

            if len(text) == 4 and int(text[3]) >= 6:
                return False

            if len(text) == 5 and int(text[4]) >= 10:
                return False

        except ValueError:
            return False

        return True

    def validar_tamanho(self, text):
        if len(text) == 0:
            return False
    
    def validar_tamanho_horario(self, text):

        for i in text:
            aux_i = i[0:2] + i[3:5]
            if i == '':
                return True
            if len(i) < 5:
                return False    
            if i[2] != ':':
                return False
            if ':' in aux_i:
                return False

class AppConsultas(ValidarEntrys, MonitorTarefas):
    # Janela principal
    def __init__(self):
        self.jan_principal = jan_principal
        self.validadores()
        self.tela_inicial()
        self.frames_principais()
        self.botoes_geral()
        self.label_status()
        self.campo_edicao_query()
        self.campos_entry()
        self.arvore()
        self.exibir_arvore()
        self.desablitar_campos()
        self.atualiz_campo_email()
        jan_principal.mainloop()        

    def limpar_campos(self):
        self.entry_nome_arquivo.delete(0, 'end')
        self.entry_nome_query.delete(0, 'end')
        self.entry_caminho_salvar.delete(0, 'end')
        self.edicao_query.delete('1.0', 'end')
        self.entry_horario1.delete(0, 'end')
        self.entry_horario2.delete(0, 'end')
        self.entry_horario3.delete(0, 'end')        
        self.entry_horario4.delete(0, 'end')
        self.entry_horario5.delete(0, 'end')
        self.entry_horario6.delete(0, 'end')
        self.entry_horario7.delete(0, 'end')
        self.entry_horario8.delete(0, 'end')
        self.entry_horario9.delete(0, 'end')
        self.entry_horario10.delete(0, 'end')
        self.entry_horario11.delete(0, 'end')
        self.entry_horario12.delete(0, 'end')

    def desablitar_campos(self):
        self.entry_nome_arquivo.config(state='readonly')
        self.entry_nome_query.config(state='readonly', foreground='black')
        self.entry_caminho_salvar.config(state='readonly', foreground='black')
        self.edicao_query.config(state='disabled', foreground='black')
        self.entry_horario1.config(state='readonly', foreground='black')
        self.entry_horario2.config(state='readonly', foreground='black')
        self.entry_horario3.config(state='readonly', foreground='black')       
        self.entry_horario4.config(state='readonly', foreground='black')
        self.entry_horario5.config(state='readonly', foreground='black')
        self.entry_horario6.config(state='readonly', foreground='black')
        self.entry_horario7.config(state='readonly', foreground='black')
        self.entry_horario8.config(state='readonly', foreground='black')
        self.entry_horario9.config(state='readonly', foreground='black')
        self.entry_horario10.config(state='readonly', foreground='black')
        self.entry_horario11.config(state='readonly', foreground='black')
        self.entry_horario12.config(state='readonly', foreground='black')
        self.entry_usu_google.config(state='readonly', foreground='black')

    def habilitar_campos(self):
        self.entry_nome_arquivo.config(state='enabled')
        self.entry_nome_query.config(state='enabled')
        self.entry_caminho_salvar.config(state='enabled')
        self.edicao_query.config(state='normal')
        self.entry_horario1.config(state='enabled')
        self.entry_horario2.config(state='enabled')
        self.entry_horario3.config(state='enabled')       
        self.entry_horario4.config(state='enabled')
        self.entry_horario5.config(state='enabled')
        self.entry_horario6.config(state='enabled')
        self.entry_horario7.config(state='enabled')
        self.entry_horario8.config(state='enabled')
        self.entry_horario9.config(state='enabled')
        self.entry_horario10.config(state='enabled')
        self.entry_horario11.config(state='enabled')
        self.entry_horario12.config(state='enabled')

    def validadores(self):
        self.valid_horario = (self.jan_principal.register(self.validar_entry_horario), '%P')
        self.valid_nome = (self.jan_principal.register(self.validar_entry_nome), '%P')

    def tela_inicial(self):

        larg_tela = self.jan_principal.winfo_screenwidth()
        altu_tela = self.jan_principal.winfo_screenheight()
        self.jan_principal.title('Agendador de consultas')
        self.jan_principal.config(bg=verde4)
        self.jan_principal.geometry('1100x600+0+0')
        self.jan_principal.minsize(width='900', height='600')
        self.jan_principal.maxsize(width='1100', height='600')

    def frames_principais(self):
        # Frame fundo
        self.frm_back = ttk.Frame(jan_principal, style='frm_back.TFrame')
        self.frm_back.place(relx=0.006, rely=0.01, relheight=0.98, relwidth=0.988)

        # Frame querys
        self.frm_querys = ttk.Frame(self.frm_back, relief='groove')
        self.etiq_querys = ttk.Label(self.frm_back, text='QUERYS:', background=verde1)
        self.frm_querys.place(relx=0.01, rely=0.05, relheight=0.4, relwidth=0.7)
        self.etiq_querys.place(relx=0.01, rely=0.02, relheight=0.03, relwidth=0.1)

        # Frame edição
        self.frm_edicao = ttk.Frame(self.frm_back, relief='groove')
        self.etiq_edicao = ttk.Label(self.frm_back, text='EDITAR QUERY:', background=verde1)
        self.frm_edicao.place(relx=0.01, rely=0.55, relheight=0.4, relwidth=0.7)
        self.etiq_edicao.place(relx=0.01, rely=0.52, relheight=0.03, relwidth=0.14)

        # Divisórias
        self.frm_divs1 = ttk.Frame(self.frm_back, relief='solid')
        self.frm_divs1.place(relx=0.72, rely=0.155, relheight=0.0022, relwidth=0.27)

    def botoes_geral(self):
        self.botao_start = ttk.Button(self.frm_back, text= 'START', command=self.acao_botao_start)
        self.botao_stop = ttk.Button(self.frm_back, text= 'STOP', command=self.acao_botao_stop)
        self.botao_start.place(relx=0.795, rely=0.72, relheight=0.07, relwidth=0.12)

        self.botao_nova_query = ttk.Button(self.frm_back, text='NOVA QUERY', command=self.acao_botao_nova_query)
        self.botao_nova_query.place(relx=0.73, rely=0.05, relheight=0.04, relwidth=0.12)
        
        self.botao_excluir_query = ttk.Button(self.frm_back, text='EXCLUIR QUERY', state='disabled', command=self.acao_botao_excluir)
        self.botao_excluir_query.place(relx=0.86, rely=0.05, relheight=0.04, relwidth=0.12)

        self.botao_editar_query = ttk.Button(self.frm_back, text='EDITAR QUERY', state='disabled', command=self.acao_botao_editar)
        self.botao_editar_query.place(relx=0.73, rely=0.10, relheight=0.04, relwidth=0.12)
        
        self.botao_limpar_campos = ttk.Button(self.frm_back, text='LIMPAR CAMPOS', state='disabled', command=self.limpar_campos)
        self.botao_limpar_campos.place(relx=0.86, rely=0.10, relheight=0.04, relwidth=0.12)

        self.botao_save = ttk.Button(self.frm_back, text='SALVAR', state='disabled', command=self.acao_botao_salvar)
        self.botao_save.place(relx=0.73, rely=0.46, relheight=0.045, relwidth=0.25)

        self.botao_exibir_monitor = ttk.Button(self.frm_back, text='EXIBIR MONITOR DE TAREFAS', state='normal', command=self.acao_botao_monitor)
        self.botao_exibir_monitor.place(relx=0.73, rely=0.60, relheight=0.060, relwidth=0.25)

        self.botao_editar_email = ttk.Button(self.frm_back, text='EDITAR', state='normal', command=self.acao_botao_editar_email)
        self.botao_editar_email.place(relx=0.896, rely=0.91, relheight=0.041, relwidth=0.05)

        self.botao_salvar_email = ttk.Button(self.frm_back, text='SALVAR', state='disabled', command=self.acao_botao_salvar_email)
        self.botao_salvar_email.place(relx=0.947, rely=0.91, relheight=0.041, relwidth=0.05)

    def label_status(self):
        self.lbl_status_programa = ttk.Label(self.frm_back, text='O programa está parado', background=vermelho0, foreground='white', font=('Calibri bold', 11), borderwidth=1, relief='groove', anchor='center')
        self.lbl_status_programa.place(relx=0.73, rely=0.80, relheight=0.05, relwidth=0.25)

    def campo_edicao_query(self):
        self.edicao_query = Text(self.frm_edicao, relief='groove')
        self.scroll_edicao_query = Scrollbar(self.frm_edicao, cursor='arrow')
        self.edicao_query.config(yscrollcommand=self.scroll_edicao_query.set, font=('consolas', 11))
        self.scroll_edicao_query.config(command=self.edicao_query.yview, cursor='arrow')
        self.edicao_query.place(relx=0.001, rely=0.0022, relheight=0.99, relwidth=0.98)
        self.scroll_edicao_query.place(anchor='ne', relx=1, rely=0.005, relheight=0.988)    

    def campos_entry(self):
        self.entry_nome_query = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_nome)
        self.etiq_entry_nome_query = ttk.Label(self.frm_back, text='QUERY:', background=verde1)
        self.entry_nome_query.place(relx=0.765, rely=0.17, relheight=0.038, relwidth=0.226, bordermode='inside')
        self.etiq_entry_nome_query.place(relx=0.715, rely=0.174)

        self.entry_nome_arquivo = ttk.Entry(self.frm_back, justify='left', state='readonly')
        self.etiq_nome_arquivo = ttk.Label(self.frm_back, text='NOME:', background=verde1)
        self.entry_nome_arquivo.place(relx=0.765, rely=0.22, relheight=0.038, relwidth=0.226)
        self.etiq_nome_arquivo.place(relx=0.715, rely=0.224)

        self.entry_caminho_salvar = ttk.Entry(self.frm_back, justify='left')
        self.etiq_entry_salvar = ttk.Label(self.frm_back, text='LOCAL:', background=verde1)
        self.entry_caminho_salvar.place(relx=0.765, rely=0.27, relheight=0.038, relwidth=0.226)
        self.etiq_entry_salvar.place(relx=0.715, rely=0.274)

        self.etiq_entry_horario1 = ttk.Label(self.frm_back, text='HORÁRIOS:', background=verde1)
        self.etiq_entry_horario1.place(relx=0.715, rely=0.324)

        self.entry_horario1 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario1.place(relx=0.80, rely=0.32, relheight=0.038, relwidth=0.04)
        self.entry_horario1.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario1.bind('<KeyRelease>', self.completar_horario)


        self.entry_horario2 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario2.place(relx=0.85, rely=0.32, relheight=0.038, relwidth=0.04)
        self.entry_horario2.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario2.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario3 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario3.place(relx=0.9, rely=0.32, relheight=0.038, relwidth=0.04)
        self.entry_horario3.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario3.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario4 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario4.place(relx=0.95, rely=0.32, relheight=0.038, relwidth=0.04)
        self.entry_horario4.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario4.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario5 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario5.place(relx=0.80, rely=0.365, relheight=0.038, relwidth=0.04)
        self.entry_horario5.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario5.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario6 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario6.place(relx=0.85, rely=0.365, relheight=0.038, relwidth=0.04)
        self.entry_horario6.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario6.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario7 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario7.place(relx=0.9, rely=0.365, relheight=0.038, relwidth=0.04)
        self.entry_horario7.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario7.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario8 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario8.place(relx=0.95, rely=0.365, relheight=0.038, relwidth=0.04)
        self.entry_horario8.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario8.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario9 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario9.place(relx=0.80, rely=0.41, relheight=0.038, relwidth=0.04)
        self.entry_horario9.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario9.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario10 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario10.place(relx=0.85, rely=0.41, relheight=0.038, relwidth=0.04)
        self.entry_horario10.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario10.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario11 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario11.place(relx=0.9, rely=0.41, relheight=0.038, relwidth=0.04)
        self.entry_horario11.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario11.bind('<KeyRelease>', self.completar_horario)

        self.entry_horario12 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario12.place(relx=0.95, rely=0.41, relheight=0.038, relwidth=0.04)
        self.entry_horario12.bind('<KeyPress>', self.completar_horario2)
        self.entry_horario12.bind('<KeyRelease>', self.completar_horario)

        self.entry_usu_google = ttk.Entry(self.frm_back, justify='left', validate='key')
        self.etiq_entry_usu_google = ttk.Label(self.frm_back, text='USUÁRIO GOOGLE:', background=verde1)
        self.entry_usu_google.place(relx=0.715, rely=0.911, relheight=0.038, relwidth=0.18)
        self.etiq_entry_usu_google.place(relx=0.715, rely=0.879)

    def completar_horario2(sef, event):
        entry_x = event.widget
        global xx
        xx = entry_x.get()

    def completar_horario(self, event):
        entry_molde =  event.widget
        texto_inserido = entry_molde.get()
        aux_molde = event.char
        aux_back = ''
        if event.keysym == 'BackSpace':
            if texto_inserido.endswith(':'):
                aux_back = 'x'
                entry_molde.delete(len(texto_inserido)-1)
            else:
                aux_back = ''
            return
        if len(texto_inserido) == 2 and not texto_inserido.endswith(':'):
            entry_molde.insert(2, ':')
            if len(xx) == 2 and aux_back == 'x':
                entry_molde.insert(3, aux_molde)
            if len(xx) == 2:
                entry_molde.insert(3, aux_molde)

    def arvore(self):
        # Definindo a árvore e suas colunas
        self.arvore_scripts = ttk.Treeview(self.frm_querys, style='arvore_scripts.Treeview')
        self.arvore_scripts['columns'] = ('Query', 'Horário', 'Nome', 'Local para salvar')
        
        self.scroll_arvore = Scrollbar(self.frm_querys, cursor='arrow', orient='vertical')
        self.arvore_scripts.config(yscrollcommand=self.scroll_arvore.set, style='Treeview')
        self.scroll_arvore.config(command=self.arvore_scripts.yview)
        self.arvore_scripts.place(relx=0.001, rely=0.002, relheight=1, relwidth=0.999)
        self.scroll_arvore.place(anchor='ne', relx=1, rely=0.005, relheight=0.992)

        # Configurando as colunas
        # Primeiro temos a coluna mãe, que possui os controles de expansão e que receberá as demais colunas:
        self.arvore_scripts.column('#0', width=1)
        # Demais colunas:
        self.arvore_scripts.column('Query', width=150, minwidth=100)
        self.arvore_scripts.column('Horário', width=70, minwidth=70)
        self.arvore_scripts.column('Nome', width=120, minwidth=120)
        self.arvore_scripts.column('Local para salvar', width=450, minwidth=100)

        # Configurando os títulos
        # Coluna mãe:
        self.arvore_scripts.heading('#0', text='')
        # Demais colunas:
        self.arvore_scripts.heading('Query', text='Query', anchor='w')
        self.arvore_scripts.heading('Horário', text='Horário', anchor='w')
        self.arvore_scripts.heading('Nome', text='Nome', anchor='w')
        self.arvore_scripts.heading('Local para salvar', text='Local para salvar', anchor='w')
        self.arvore_scripts.tag_configure('x1', background=verde_claro)
        self.arvore_scripts.tag_configure('x2', background='white')
        self.arvore_scripts.bind('<ButtonRelease-1>', self.selecionar_item_arvore)
        self.arvore_scripts.bind('<KeyRelease-Down>', self.selecionar_item_arvore)
        self.arvore_scripts.bind('<KeyRelease-Up>', self.selecionar_item_arvore)

    def exibir_arvore(self):
        for i in self.arvore_scripts.get_children():
            self.arvore_scripts.delete(i)
        try:
            with open(CAMINHO_DB_JSON, 'r', encoding='utf8') as js:
                dados_exibir_arvore = json.load(js)
                count_pai = 0
                tag = 'x1'

                for item, valor in dados_exibir_arvore.items():
                    tag ='x1' if (count_pai % 2) == 0 else 'x2'

                    self.arvore_scripts.insert(parent='', index='end', iid=count_pai, text='', values=(item, '', valor['nome'], valor['caminho_salvar']), tags=tag)
                    count_filho = 0
                    for ext_hora in valor['horario']:
                        
                        if ext_hora != '':
                            id_aux = f'{count_pai}.{count_filho}'
                            self.arvore_scripts.insert(parent='', index='end', iid=id_aux, text='', values=('    '+item, '    '+ext_hora, '    '+valor['nome'],'    '+valor['caminho_salvar']), tags=tag)
                            self.arvore_scripts.move(id_aux, count_pai, count_filho)
                            count_filho += 1
                    count_pai += 1
        except:
            pass

    def selecionar_item_arvore(self, event):
        # Apagar dados das entry
        self.habilitar_campos()
        self.limpar_campos()
        self.atualiz_campo_email()

        # inputar dados nas entrys
        try:
            linha_selec = self.arvore_scripts.selection()[0]
            dados_selec = self.arvore_scripts.item(linha_selec, "values")
            with open(CAMINHO_DB_JSON, 'r', encoding='utf-8') as js_sel:
                dados_finais = json.load(js_sel)
                name_qry = dados_selec[0].strip()
                horarios = dados_finais[name_qry.strip()]['horario']
                name_arq = dados_finais[name_qry.strip()]['nome']
                loc_salvar = dados_finais[name_qry.strip()]['caminho_salvar']
                queryx = dados_finais[name_qry.strip()]['query']

            self.entry_nome_query.insert(0, name_qry)        
            self.entry_nome_arquivo.insert(0, name_arq)        
            self.entry_caminho_salvar.insert(0, loc_salvar)        
            self.edicao_query.insert(1.0, queryx)
            self.entry_horario1.insert(0, horarios[0])
            self.entry_horario2.insert(0, horarios[1])
            self.entry_horario3.insert(0, horarios[2])
            self.entry_horario4.insert(0, horarios[3])
            self.entry_horario5.insert(0, horarios[4])
            self.entry_horario6.insert(0, horarios[5])
            self.entry_horario7.insert(0, horarios[6])
            self.entry_horario8.insert(0, horarios[7])
            self.entry_horario9.insert(0, horarios[8])
            self.entry_horario10.insert(0, horarios[9])
            self.entry_horario11.insert(0, horarios[10])
            self.entry_horario12.insert(0, horarios[11])
            self.desablitar_campos()
            if estado_programa.obtem_status() == 'Executando':
                #self.botao_start['state'] = 'normal'
                self.botao_editar_query['state'] = 'disabled'
                self.botao_excluir_query['state'] = 'disabled'
                self.botao_nova_query['state'] = 'disabled'
                self.botao_limpar_campos['state'] = 'disabled'
                self.botao_save['state'] = 'disabled'
            elif estado_programa.obtem_status() in ['Parado', 'Inicio']:
                self.botao_start['state'] = 'normal'
                self.botao_editar_query['state'] = 'normal'
                self.botao_excluir_query['state'] = 'normal'
                self.botao_nova_query['state'] = 'normal'
                self.botao_limpar_campos['state'] = 'disabled'
                self.botao_save['state'] = 'disabled'
        except IndexError:
            pass
        
    def acao_botao_nova_query(self):
        self.atualiz_campo_email()
        global nome_antigo_query
        nome_antigo_query = ''
        if estado_programa.obtem_status() == 'Executando':
            pass
        else:
            self.botao_start['state'] = 'disabled'
            self.botao_editar_query['state'] = 'disabled'
            self.botao_excluir_query['state'] = 'disabled'
            self.botao_nova_query['state'] = 'disabled'
            self.botao_limpar_campos['state'] = 'normal'
            self.botao_save['state'] = 'normal'
            self.botao_editar_email['state'] = 'disabled'
            try:
                self.arvore_scripts.selection_remove(self.arvore_scripts.selection()[0])
            except:
                pass
            self.habilitar_campos()
            self.limpar_campos()

    def acao_botao_editar(self):
        self.atualiz_campo_email()
        global nome_antigo_query
        nome_antigo_query = self.entry_nome_query.get().strip()
        self.botao_start['state'] = 'disabled'
        self.botao_nova_query['state'] = 'disabled'
        self.botao_excluir_query['state'] = 'disabled'
        self.botao_editar_query['state'] = 'disabled'
        self.botao_limpar_campos['state'] = 'normal'
        self.botao_save['state'] = 'normal'
        self.botao_editar_email['state'] = 'disabled'

        self.habilitar_campos()

    def acao_botao_excluir(self):
        self.atualiz_campo_email()
        nome_antigo_query = self.entry_nome_query.get().strip()
        if messagebox.askyesno('Excluir', f'Deseja excluir a query "{nome_antigo_query}"'):
            with open(CAMINHO_DB_JSON, 'r', encoding='utf-8') as arquivojs2, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as jstemporario2:
                dados_temp2 = json.load(arquivojs2)
                dados_temp2.pop(nome_antigo_query)
                json.dump(dados_temp2, jstemporario2, ensure_ascii=False)
            shutil.move(jstemporario2.name, CAMINHO_DB_JSON)
            self.habilitar_campos()
            self.limpar_campos()
            self.desablitar_campos()
            self.exibir_arvore()
            self.botao_editar_query['state'] = 'disabled'
            self.botao_excluir_query['state'] = 'disabled'
            obter_cronograma_status()
        
    def acao_botao_stop(self):
        self.atualiz_campo_email()
        estado_programa.define_status('Parado')
        self.lbl_status_programa.config(text='O programa está parado', background=vermelho0, foreground='white')
        self.botao_stop['state'] = 'disabled'
        self.botao_stop.place_forget()
        self.botao_start.place(relx=0.795, rely=0.72, relheight=0.07, relwidth=0.12)
        self.botao_start['state'] = 'normal'
        self.botao_nova_query['state'] = 'normal'
        self.botao_editar_query['state'] = 'normal'
        self.botao_excluir_query['state'] = 'normal'
        self.botao_salvar_email['state'] = 'disabled'
        self.botao_editar_email['state'] = 'normal'
        click_start_stop()

    def acao_botao_salvar(self):
        # Obtém os dados inputados pelo usuário
        nome_query_salvar = self.entry_nome_query.get().strip()
        horarios_query = sorted([self.entry_horario1.get(), self.entry_horario2.get(), self.entry_horario3.get(), self.entry_horario4.get(), self.entry_horario5.get(),
                self.entry_horario6.get(), self.entry_horario7.get(), self.entry_horario8.get(), self.entry_horario9.get(), self.entry_horario10.get(), 
                self.entry_horario11.get(), self.entry_horario12.get()], key = lambda x: (x is '', x))
        nome_arquivo = self.entry_nome_arquivo.get().strip()
        caminho_salvar_query = self.entry_caminho_salvar.get()
        query_script = self.edicao_query.get('1.0', 'end-1c')


            
        if self.validar_tamanho(nome_query_salvar) is False:
            messagebox.showerror('NOME INVÁLIDO', 'QUERY: O nome inserido para a query é inválido. \nOs dados não foram salvos.')
            
        elif self.validar_tamanho(nome_arquivo) is False:
            messagebox.showerror('NOME INVÁLIDO', 'NOME: o nome inserido para o arquivo é inválido. \nOs dados não foram salvos.')
        
        elif os.path.isdir(caminho_salvar_query) is False:
            messagebox.showerror('CAMINHO INVÁLIDO', 'LOCAL: O caminho inserido para salvamento não é válido. \nOs dados não foram salvos.')

        elif self.validar_tamanho_horario(horarios_query) is False:
            messagebox.showerror('HORÁRIO INVÁLIDO', 'HORÁRIO: O horário inserido não é válido. \nOs dados não foram salvos.')
        

        else:
            dados_script = {
                    nome_query_salvar : {
                    "horario": horarios_query,
                    "nome": nome_arquivo,
                    "caminho_salvar": caminho_salvar_query,
                    "query": query_script
                    }
                }

            # Gambiarra alert: utilizaremos um arquivo temporário para que as modificações não ocorram diretamente no JSON.
            #   Abriremos o arquivo JSON 
            with open(CAMINHO_DB_JSON, 'r', encoding='utf-8') as arquivojs, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as jstemporario:
                # Traremos os dados para uma variável:
                try:
                    dados_temp = json.load(arquivojs)
                except:
                    dados_temp = {}
                validar_nome_existe = []

                for x in dados_temp:
                    validar_nome_existe.append(str(x).upper())

                if nome_antigo_query == '':
                    if nome_query_salvar.upper() in validar_nome_existe:
                        messagebox.showerror('DUPLICIDADE', f'Já existe uma query com o nome "{nome_query_salvar}". \nInsira um novo nome.')
                    elif messagebox.askyesno('SALVAR NOVA QUERY', f'Deseja salvar uma nova query com o nome "{nome_query_salvar}"?'):
                        dados_temp.update(dados_script)
                        self.limpar_campos()
                        self.desablitar_campos()
                        self.botao_editar_query['state'] = 'disabled'
                        self.botao_save['state'] = 'disabled'
                        self.botao_limpar_campos['state'] = 'disabled'
                        self.botao_nova_query['state'] = 'normal'

                else:
                    if nome_query_salvar.upper() in validar_nome_existe:
                        if nome_query_salvar.upper() == nome_antigo_query.upper():
                            if messagebox.askyesno('EDITAR', f'Deseja sobrescrever os dados da query "{nome_antigo_query}"?'):
                                dados_temp.pop(nome_antigo_query)
                                dados_temp.update(dados_script)
                                self.limpar_campos()
                                self.desablitar_campos()
                                self.botao_editar_query['state'] = 'disabled'
                                self.botao_save['state'] = 'disabled'
                                self.botao_limpar_campos['state'] = 'disabled'
                                self.botao_nova_query['state'] = 'normal'
                                
                        else:
                            messagebox.showerror('DUPLICIDADE', f'Já existe uma query com o nome "{nome_query_salvar}". \nInsira um novo nome.')
                    else:
                        if messagebox.askyesno('EDITAR', f'Deseja sobrescrever os dados da query "{nome_antigo_query}"?'):
                                dados_temp.pop(nome_antigo_query)
                                dados_temp.update(dados_script)
                                self.limpar_campos()
                                self.desablitar_campos()
                                self.botao_editar_query['state'] = 'disabled'
                                self.botao_save['state'] = 'disabled'
                                self.botao_limpar_campos['state'] = 'disabled'
                                self.botao_nova_query['state'] = 'normal'

                # Por fim, sobe os dados temporários, alterados ou não, para o JSON:
                dados_temp_org = dict(sorted(dados_temp.items(), key=lambda x: x[0]))

                json.dump(dados_temp_org, jstemporario,indent=4, ensure_ascii=False)

            shutil.move(jstemporario.name, CAMINHO_DB_JSON)

            self.botao_start['state'] = 'normal'
            self.exibir_arvore()
            self.atualiz_campo_email()
            obter_cronograma_status()

    def acao_botao_monitor(self):
        if not any(isinstance(x, Toplevel) for x in jan_principal.winfo_children()):
            MonitorTarefas()
        else:
            pass

    def acao_botao_editar_email(self):
        self.botao_editar_email['state'] = 'disabled'
        self.botao_salvar_email['state'] = 'normal'
        self.entry_usu_google.config(state='enabled')

    def acao_botao_salvar_email(self):
        self.botao_salvar_email['state'] = 'disabled'
        self.botao_editar_email['state'] = 'normal'
        self.entry_usu_google.config(state='disabled')
        with open(CAMINHO_DB_EMAIL, 'w', encoding='utf-8') as base_email:
            email_capturado = self.entry_usu_google.get()
            json.dump(email_capturado, base_email, indent=4, ensure_ascii=False)


    def atualiz_campo_email(self):
        if self.entry_usu_google['state'] == 'enabled':
            self.entry_usu_google.delete(0, 'end')
        else:
            self.entry_usu_google['state'] = 'enabled'
            self.entry_usu_google.delete(0, 'end')
        try:
            with open(CAMINHO_DB_EMAIL, 'r', encoding='utf-8') as temp_leitura_email:
                email_entrada = json.load(temp_leitura_email)
                self.entry_usu_google.insert(0, email_entrada)
        except FileNotFoundError:
            with open(CAMINHO_DB_EMAIL, 'w', encoding='utf-8') as novo_arq:
                email_entrada = []
                json.dump(email_entrada, novo_arq, indent=4, ensure_ascii=False)

        self.botao_editar_email['state'] = 'enabled'
        self.botao_salvar_email['state'] = 'disabled'
        self.entry_usu_google['state'] = 'disabled'

    def acao_botao_start(self):
        self.atualiz_campo_email()
        
        try:
            with open(CAMINHO_DB_JSON, 'r', encoding='utf-8') as temp_verif:
                validar_base = json.load(temp_verif)
                if validar_base == {}:
                    messagebox.showerror('ERRO', 'Não existem tarefas a serem executadas!')
                else:
                    estado_programa.define_status('Executando')
                    self.habilitar_campos()
                    self.limpar_campos()
                    self.desablitar_campos()
                    self.botao_nova_query['state'] = 'disabled'
                    self.botao_excluir_query['state'] = 'disabled'
                    self.botao_editar_query['state'] = 'disabled'
                    self.botao_limpar_campos['state'] = 'disabled'
                    self.botao_save['state'] = 'disabled'
                    self.botao_salvar_email['state'] = 'disabled'
                    self.botao_editar_email['state'] = 'disabled'
                    self.lbl_status_programa.config(text='O programa está executando', background=verde_status, foreground='white')
                    self.botao_start['state'] = 'disabled'
                    self.botao_start.place_forget()
                    self.botao_stop.place(relx=0.795, rely=0.72, relheight=0.07, relwidth=0.12)
                    self.botao_stop['state'] = 'normal'
                    click_start_stop()


        except:
            messagebox.showerror('ERRO', 'Base de dados não encontrada')

if __name__ == '__main__':
    AppConsultas()
