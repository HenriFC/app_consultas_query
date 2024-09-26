import os
import json
import shutil
import tempfile
import threading
import time
from playwright.sync_api import sync_playwright
from datetime import date, datetime, timedelta
from cronograma_geral import obter_cronograma_status
from state_exec import estado_programa, estado_database



PASTA_LOGS = 'logs_exec_tarefas'
CAMINHO_ARQ = 'database_cronograma.json'
CAMINHO_DB_EMAIL = 'database_email.json'


if not os.path.exists(PASTA_LOGS):
    os.makedirs(PASTA_LOGS)

def obter_email():
    with open(CAMINHO_DB_EMAIL, 'r', encoding='utf-8') as temp_email:
        dados = json.load(temp_email)
        email_entrada = dados["EMAIL"]
        print("lendo email")
    return email_entrada

def obter_link():
    with open(CAMINHO_DB_EMAIL, 'r', encoding='utf-8') as temp_email:
        dados = json.load(temp_email)
        link = dados["LINK"]
        print("lendo email")
    return link



class GerenciadorTarefas:
    def __init__(self):
        self.threads_tarefas = []
        self.executando = estado_programa.obtem_status()
        self.data_atual = date.today().strftime('%d.%m.%Y')
        self.horario_atual = datetime.now().strftime('%H:%M') + ':00'
        self.base_atualizada = []
        self.lock = threading.Lock()

    def iniciar(self):
        # Função da thread gerenciadora para monitorar e iniciar tarefas.
        while True:
            with self.lock:
                self.data_atual = date.today().strftime('%d.%m.%Y')
                self.horario_atual = datetime.now().strftime('%H:%M') + ':00'
                self.base_atualizada = []
                self.atualiz_item = []
                if self.executando == 'Executando':
                    with open(CAMINHO_ARQ, 'r', encoding='utf-8') as crono_original, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
                        extracao = json.load(crono_original)
                        for item, detal in enumerate(extracao):
                            if detal['HORA_INICIO_PLAN'] == self.horario_atual and detal["STATUS"] == 'Pendente' and detal['DATA'] == self.data_atual:
                                self.atualiz_item = extracao[item]
                                self.atualiz_item['STATUS'] = 'Executando'
                                self.base_atualizada.append(self.atualiz_item)
                                id_tarefa = detal['ID']
                                hr_ini_consulta = detal['HORA_INICIO_CONS']
                                hr_fim_consulta = detal['HORA_FIM_CONS']
                                nome_arq = detal['NOME_ARQUIVO']
                                cod_query = detal['QUERY']
                                caminho_salvar_arq = detal['CAMINHO_SALVAR']
                                email_entrada = obter_email()
                                link = obter_link()
                                print(email_entrada)
                                # Inicia essa tarefa:
                                self.iniciar_tarefa(id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, cod_query, caminho_salvar_arq, email_entrada, link)
                            else:
                                self.base_atualizada.append(extracao[item])
                        
                        json.dump(self.base_atualizada, file_temp,indent=4, ensure_ascii=False)
                    shutil.move(file_temp.name, CAMINHO_ARQ)
                    obter_cronograma_status()
                    
            time.sleep(1)  # Aguarda antes de verificar novamente

    def iniciar_tarefa(self, id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, cod_query, caminho_salvar_arq, email_entrada, link):
        # Inicia uma nova tarefa em uma thread separada
        thread_tarefa = threading.Thread(target=self.executar_tarefa, args=(id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, cod_query, caminho_salvar_arq, email_entrada, link))
        thread_tarefa.start()
        self.threads_tarefas.append(thread_tarefa)

    def executar_tarefa(self, id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, cod_query, caminho_salvar_arq, email_entrada, link):
        # Iniciar criando um arquivo para receber o log das tarefas
        # Esse arquivo receberá os horários de inicío e fim, erros e etc
        # Sempre que necessário, durante a execução, dumpará informações específicas nesse arquivo, porém o arquivo de dump será um JSON com campos padronizados
        print(f'[{threading.current_thread().name}] {id_tarefa} iniciada.')
        time.sleep(1)

        with sync_playwright() as pw:
            # Iniciar edge:
            navegador = pw.chromium.launch(channel='msedge', headless=False)
            pagina = navegador.new_page()

            pagina.goto(link)


            # Obter campos login:
            pagina.wait_for_selector('xpath=//*[@id="identifierId"]')
            print('encerrou a espera pelo campo "email"')
            campo_inserir_email = pagina.locator('xpath=//*[@id="identifierId"]')

            pagina.wait_for_selector('xpath=//*[@id="identifierNext"]/div/button/span')
            print('encerrou a espera pelo botão"')
            botao_proxima = pagina.locator('xpath=//*[@id="identifierNext"]/div/button/span')

            campo_inserir_email.fill(email_entrada)
            botao_proxima.click()

            # Dentro da BigQuery: Verificar carregamento da página.
            print('Dentro da Bigquery. Verificando se carregou corretamente')
            # verifica se a logo do Google está presente
            pagina.wait_for_selector('xpath=//*[@id="_0rif_mat-tab-link-4"]/span[2]')
            print('Logo Google encontrado')
            # verifica se a lupa da bigquery está presente
            pagina.wait_for_selector('xpath=//*[@id="panelgoog_1256029785"]/xap-deferred-loader-outlet/pcc-section-nav-bar/div/cfc-section-title/h2/button/cfc-icon[1]/mat-icon/svg')
            print('Lupa bigquery encontrada')
            # verifica se a aba "Consulta sem título" está presente
            pagina.wait_for_selector('xpath=//*[@id="_0rif_mat-tab-link-4"]/span[2]')
            print('Aba "Consulta sem título" encontrada')



            # Clicar na aba "Consulta sem título":
            aba_consulta_em_branco = pagina.locator('xpath=//*[@id="_0rif_mat-tab-link-4"]/span[2]')
            aba_consulta_em_branco.click()

            # Verificar se o campo para inserir código query está presente:
            pagina.wait_for_selector('xpath=//*[@id="_0rif_panelgoog_1520729473"]/cfc-panel-body/cfc-virtual-viewport/div[1]/bqui-query-editor/shared-query-editor/div/div[3]/div/cfc-code-editor/div/div/div/div[1]/div[2]/div[1]/div[4]')
            print('Campo de inserção de consultas encontrado')
            area_digitar_query = pagina.locator('xpath=//*[@id="_0rif_panelgoog_1520729473"]/cfc-panel-body/cfc-virtual-viewport/div[1]/bqui-query-editor/shared-query-editor/div/div[3]/div/cfc-code-editor/div/div/div/div[1]/div[2]/div[1]/div[4]')
            area_digitar_query.click()
            area_digitar_query.fill(cod_query)


            pagina.pause()


        print(f"[{threading.current_thread().name}] {id_tarefa} concluída.")

    def dump_infos_exec(self, ):

        pass
    def click_botao(self):
        # Define o estado como executando e inicia novas tarefas
        with self.lock:
            self.executando = estado_programa.obtem_status()


# Inicializando o gerenciador e a thread gerenciadora
gerenciador = GerenciadorTarefas()
thread_gerenciadora = threading.Thread(target=gerenciador.iniciar, daemon=True)
thread_gerenciadora.start()

# Funções para simular cliques nos botões START e STOP
def click_start_stop():
    gerenciador.click_botao()
    print('START/STOP pressionado.')
