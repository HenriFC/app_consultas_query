import os
import json
import shutil
import tempfile
from tkinter import Tk, PhotoImage, Scrollbar, Text
from tkinter import ttk
from tkinter import messagebox


from autoedge import iniciar_edge
from coreslayout import *
from verificacoes import validar_entry

jan_principal = Tk()
img = PhotoImage(file='icon2.png')
jan_principal.iconphoto(True, img)
s = ttk.Style()
s.configure('frm_status_start.TFrame', background=verde0)
s.configure('frm_status_stop.TFrame', background=vermelho0)
s.configure('frm_back.TFrame', background=verde1)
caminho_json = 'database.json'



class funcoes():
    def __init__(self) -> None:
        self.iniciar_db()


    def iniciar_db(self):

        return

    def selecionar_item(self):

        return
    
    def limpar_campos(self):
        return
    
    def add_(self):
        self.namex = self.entry.get()
        

        return


class app_consultas(validar_entry):
    # Janela principal
    def __init__(self):
        self.jan_principal = jan_principal
        self.validadores()
        self.tela_inicial()
        self.frames_principais()
        self.botoes_geral()
        self.label_status()
        self.arvore()
        self.campo_edicao_query()
        self.campos_entry()
        self.exibir_arvore()
        jan_principal.mainloop()
    
    # Abrir o JSON contendo os dados

    def validadores(self):
        self.valid_horario = (self.jan_principal.register(self.validar_entry_horario), '%P')
        self.valid_nome = (self.jan_principal.register(self.validar_entry_nome), '%P')

    # Quadrante onde alocaremos as opções
    def tela_inicial(self):
        self.jan_principal.title('Agendador de consultas')
        self.jan_principal.config(bg=verde4, )
        self.jan_principal.geometry('900x600')
        self.jan_principal.minsize(width='900', height='600')
        self.jan_principal.maxsize(width='900', height='600')

    def frames_principais(self):
        # Frame fundo
        self.frm_back = ttk.Frame(jan_principal, width=790, height=590, style='frm_back.TFrame')
        self.frm_back.place(relx=0.006, rely=0.01, relheight=0.98, relwidth=0.988)

        # Frame querys
        self.frm_querys = ttk.Frame(self.frm_back, relief='groove')
        self.etiq_querys = ttk.Label(self.frm_back, text='QUERYS:', background=verde1)
        self.frm_querys.place(relx=0.01, rely=0.05, relwidth=0.7, relheight=0.43)
        self.etiq_querys.place(relx=0.01, rely=0.02, relheight=0.03, relwidth=0.1)

        self.frm_divs1 = ttk.Frame(self.frm_back, relief='solid')
        self.frm_divs1.place(relx=0.72, rely=0.17, relheight=0.0022, relwidth=0.27)

        # Frame edição
        self.frm_edicao = ttk.Frame(self.frm_back, relief='groove')
        self.etiq_edicao = ttk.Label(self.frm_back, text='EDITAR QUERY:', background=verde1)
        self.frm_edicao.place(relx=0.01, rely=0.55, relheight=0.4, relwidth=0.7)
        self.etiq_edicao.place(relx=0.01, rely=0.52, relheight=0.03, relwidth=0.14)

    def botoes_geral(self):
        self.botao_start = ttk.Button(self.frm_back, text= 'START', command=self.acao_botao_start)
        self.botao_stop = ttk.Button(self.frm_back, text= 'STOP', command=self.acao_botao_stop)
        self.botao_start.place(relx=0.795, rely=0.80, relheight=0.07, relwidth=0.12)

        self.botao_save = ttk.Button(self.frm_back, text='SALVAR', command=self.acao_botao_salvar)
        self.botao_save.place(relx=0.46, rely=0.95, relheight=0.045, relwidth=0.1)

        self.botao_nova_query = ttk.Button(self.frm_back, text='NOVA QUERY', command=self.acao_botao_nova_query)
        self.botao_nova_query.place(relx=0.73, rely=0.10, relheight=0.04, relwidth=0.12)
        
        self.botao_excluir_query = ttk.Button(self.frm_back, text='EXCLUIR QUERY', command=funcoes.limpar_campos)
        self.botao_excluir_query.place(relx=0.86, rely=0.10, relheight=0.04, relwidth=0.12)

        self.botao_ok = ttk.Button(self.frm_back, text='OK', state='disabled', command=self.acao_botao_ok)
        self.botao_ok.place(relx=0.94, rely=0.048, relheight=0.043, relwidth=0.04)

    def label_status(self):
        self.lbl_status_programa = ttk.Label(self.frm_back, text='O programa está parado', background=vermelho0, borderwidth=1, relief='groove', anchor='center')
        self.lbl_status_programa.place(relx=0.73, rely=0.88, relheight=0.05, relwidth=0.25)

    def campo_edicao_query(self):
        self.edicao_query = Text(self.frm_edicao)
        self.scroll_edicao_query = Scrollbar(self.frm_edicao, cursor='arrow')
        self.edicao_query.config(yscrollcommand=self.scroll_edicao_query.set, font=('consolas', 11))
        self.scroll_edicao_query.config(command=self.edicao_query.yview, cursor='arrow')
        self.edicao_query.place(relx=0.001, rely=0.0022, relheight=0.99, relwidth=0.97)
        self.scroll_edicao_query.place(relx=0.97, rely=0.01, relheight=0.97)    

    def campos_entry(self):
        self.entry_nova_query = ttk.Entry(self.frm_back, justify='left', state='disabled')
        self.etiq_nova_query = ttk.Label(self.frm_back, text='NOME QUERY:', background=verde1)
        self.entry_nova_query.place(relx=0.73, rely=0.05, relheight=0.04, relwidth=0.21)
        self.etiq_nova_query.place(relx=0.73, rely=0.02, relheight=0.03, relwidth=0.1)

        self.entry_nome = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_nome)
        self.etiq_entry_nome = ttk.Label(self.frm_back, text='NOME:', background=verde1)
        self.entry_nome.place(relx=0.78, rely=0.195, relheight=0.038, relwidth=0.21)
        self.etiq_entry_nome.place(relx=0.72, rely=0.20)

        self.entry_salvar = ttk.Entry(self.frm_back, justify='left')
        self.etiq_entry_salvar = ttk.Label(self.frm_back, text='SALVAR:', background=verde1)
        self.entry_salvar.place(relx=0.78, rely=0.245, relheight=0.038, relwidth=0.21)
        self.etiq_entry_salvar.place(relx=0.72, rely=0.25)

        self.etiq_entry_horario1 = ttk.Label(self.frm_back, text='HORÁRIOS:', background=verde1)
        self.etiq_entry_horario1.place(relx=0.72, rely=0.30)

        self.entry_horario1 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario1.place(relx=0.80, rely=0.295, relheight=0.038, relwidth=0.04)

        self.entry_horario2 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario2.place(relx=0.85, rely=0.295, relheight=0.038, relwidth=0.04)

        self.entry_horario3 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario3.place(relx=0.9, rely=0.295, relheight=0.038, relwidth=0.04)

        self.entry_horario4 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario4.place(relx=0.95, rely=0.295, relheight=0.038, relwidth=0.04)

        self.entry_horario5 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario5.place(relx=0.80, rely=0.35, relheight=0.038, relwidth=0.04)

        self.entry_horario6 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario6.place(relx=0.85, rely=0.35, relheight=0.038, relwidth=0.04)

        self.entry_horario7 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario7.place(relx=0.9, rely=0.35, relheight=0.038, relwidth=0.04)

        self.entry_horario8 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario8.place(relx=0.95, rely=0.35, relheight=0.038, relwidth=0.04)

        self.entry_horario9 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario9.place(relx=0.80, rely=0.405, relheight=0.038, relwidth=0.04)

        self.entry_horario10 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario10.place(relx=0.85, rely=0.405, relheight=0.038, relwidth=0.04)

        self.entry_horario11 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario11.place(relx=0.9, rely=0.405, relheight=0.038, relwidth=0.04)

        self.entry_horario12 = ttk.Entry(self.frm_back, justify='left', validate='key', validatecommand=self.valid_horario)
        self.entry_horario12.place(relx=0.95, rely=0.405, relheight=0.038, relwidth=0.04)

    def arvore(self):
        # Definindo a árvore e suas colunas
        self.arvore_scripts = ttk.Treeview(self.frm_querys)
        self.arvore_scripts['columns'] = ('Query', 'Horário', 'Local para salvar')
        
        self.scroll_arvore = Scrollbar(self.frm_querys, cursor='arrow')
        self.arvore_scripts.config(yscrollcommand=self.scroll_arvore.set)
        self.scroll_arvore.config(command=self.arvore_scripts.yview)
        self.arvore_scripts.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.scroll_arvore.place(relx=0.972, rely=0.005, relheight=0.991)

        # Configurando as colunas
        # Primeiro temos a coluna mãe, que possui os controles de expansão e que receberá as demais colunas:
        self.arvore_scripts.column('#0', width=1)
        # Demais colunas:
        self.arvore_scripts.column('Query', width=150, minwidth=100)
        self.arvore_scripts.column('Horário', width=70, minwidth=100)
        self.arvore_scripts.column('Local para salvar', width=450, minwidth=100)

        # Configurando os títulos
        # Coluna mãe:
        self.arvore_scripts.heading('#0', text='')
        # Demais colunas:
        self.arvore_scripts.heading('Query', text='Query', anchor='w')
        self.arvore_scripts.heading('Horário', text='Horário', anchor='w')
        self.arvore_scripts.heading('Local para salvar', text='Local para salvar', anchor='w')
        self.arvore_scripts.tag_configure('x1', background=verde_claro)
        self.arvore_scripts.tag_configure('x2', background='white')

        # Imputando dados

    def exibir_arvore(self):
        for i in self.arvore_scripts.get_children():
            self.arvore_scripts.delete(i)
        with open(caminho_json, 'r', encoding='utf8') as js:
            dados_exibir_arvore = json.load(js)
            count_pai = 0
            tag = 'x1'

            for item, valor in dados_exibir_arvore.items():
                tag ='x1' if (count_pai % 2) == 0 else 'x2'
                print(item)
                self.arvore_scripts.insert(parent='', index='end', iid=count_pai, text='', values=(item, '', valor['caminho_salvar']), tags=tag)
                count_filho = 0
                for ext_hora in valor['horario']:
                    
                    if ext_hora != '':
                        id_aux = f'{count_pai}.{count_filho}'
                        print(ext_hora)
                        print(id_aux)
                        self.arvore_scripts.insert(parent='', index='end', iid=id_aux, text='', values=('    '+item, '    '+ext_hora, '    '+valor['caminho_salvar']), tags=tag)
                        self.arvore_scripts.move(id_aux, count_pai, count_filho)
                        count_filho += 1
                count_pai += 1

    def selecionar_item_arvore(Self):
        # Apagar dados das entry

        # Obter dados da linha selecionada

        # inputar dados nas entrys


        return

    def alterar_nome_query(sef):


        


        return



    def acao_botao_nova_query(self):
        self.entry_nova_query['state'] = 'NORMAL'
        self.botao_ok['state'] = 'NORMAL'
        
    def acao_botao_ok(self):
        nova_query_nome = self.entry_nova_query.get()


    def acao_botao_start(self):
        self.lbl_status_programa.config(text='O programa está executando', background=verde0)
        self.botao_start.place_forget()
        self.botao_stop.place(relx=0.795, rely=0.80, relheight=0.07, relwidth=0.12)

    def acao_botao_stop(self):
        self.lbl_status_programa.config(text='O programa está parado', background=vermelho0)
        self.botao_stop.place_forget()
        self.botao_start.place(relx=0.795, rely=0.80, relheight=0.07, relwidth=0.12)

    def acao_botao_salvar(self):
        # Obtém os dados inputados pelo usuário
        nome_query = self.entry_nome.get().strip()
        caminho_salvar_query = self.entry_salvar.get()
        horarios_query = [self.entry_horario1.get(), self.entry_horario2.get(), self.entry_horario3.get(), self.entry_horario4.get(), self.entry_horario5.get(),
                        self.entry_horario6.get(), self.entry_horario7.get(), self.entry_horario8.get(), self.entry_horario9.get(), self.entry_horario10.get(), 
                        self.entry_horario11.get(), self.entry_horario12.get()]
        query_script = self.edicao_query.get('1.0', 'end-1c')

        
        # Verifica se o caminho para salvar é válido
        if os.path.isdir(caminho_salvar_query) is False:
            messagebox.showerror('Caminho inválido', 'O caminho inserido para salvamento não é válido.') 

        elif nome_query == '':
            messagebox.showinfo('Nome inválido', 'O nome inserido é inválido. Os dados não foram salvos.')
    
        else:
            dados_script = {
                nome_query : {
                    "caminho_salvar": caminho_salvar_query,
                    "horario": horarios_query,
                    "query": query_script
                    }
                }

            # Gambiarra alert: utilizaremos um arquivo temporário para que as modificações não ocorram diretamente no JSON.
            #   Abriremos o arquivo JSON 
            with open(caminho_json, 'r', encoding='utf-8') as arquivojs, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as jstemporario:
                # Traremos os dados para uma variável:
                try:
                    dados_temp = json.load(arquivojs)
                except:
                    dados_temp = {}


                # Verificamos se os nome da query já está no JSON. Caso esteja, perguntaremos ao usuário se deseja atualizar os dados
                if nome_query in dados_temp:
                    if messagebox.askyesno('Salvar', f'Deseja sobrescrever os dados da query "{nome_query}"?'):
                        dados_temp.update(dados_script)
                # Se o nome da query não existir no JSON, perguntaremos se realmente deseja salvar um novo registro
                else:
                    if messagebox.askyesno('Salvar', f'Deseja salvar uma nova query com o nome "{nome_query}"?'):
                        dados_temp.update(dados_script)
                # Por fim, sobe os dados temporários, alterados ou não, para o JSON:
                json.dump(dados_temp, jstemporario, ensure_ascii=False)

            shutil.move(jstemporario.name, caminho_json)
            print("*" * 150)
        self.exibir_arvore()
        
    





app_consultas()


