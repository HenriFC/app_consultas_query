import os
import json
import shutil
import tempfile
import threading
import time
from pyautogui import press
from playwright.sync_api import sync_playwright, expect
from datetime import date, datetime, timedelta
from cronograma_geral import obter_cronograma_status
from state_exec import estado_programa, estado_database



PASTA_LOGS = 'logs_exec_tarefas'
PASTA_DOWNLOAD_TEMP = 'downloads_temp'
CAMINHO_ARQ = 'database_cronograma.json'
CAMINHO_DB_EMAIL = 'database_email.json'


if not os.path.exists(PASTA_LOGS):
    os.makedirs(PASTA_LOGS)

if not os.path.exists(PASTA_DOWNLOAD_TEMP):
    os.makedirs(PASTA_DOWNLOAD_TEMP)

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
                    for i in range(10): 
                        try:
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
                                        link = detal['QUERY']
                                        print(email_entrada)
                                        # Inicia essa tarefa:
                                        self.iniciar_tarefa(id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, cod_query, caminho_salvar_arq, email_entrada, link)
                                    else:
                                        self.base_atualizada.append(extracao[item])
                                
                                json.dump(self.base_atualizada, file_temp,indent=4, ensure_ascii=False)
                                print(f'{i} - FOR loop iniciar executado')
                                press('shift')                         
                            shutil.move(file_temp.name, CAMINHO_ARQ)
                            obter_cronograma_status()
                            break
                        except:
                            time.sleep(1)
                        
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
            caminho_download_temp = os.path.join(PASTA_DOWNLOAD_TEMP, nome_arq)
            caminho_download_final = os.path.join(caminho_salvar_arq, nome_arq)

            def inserir_email(pagina, tentativas=10, timeout=2000):
                # Aguardando a página de login
                pagina.wait_for_selector('xpath=//*[@id="identifierId"]', timeout=120000)
                print('encerrou a espera pelo campo "email"')
                pagina.wait_for_selector('xpath=//*[@id="identifierNext"]/div/button/span', timeout=120000)
                print('encerrou a espera pelo botão "Próximo"')
                for i in range(tentativas):
                    try:
                        pagina.wait_for_selector('xpath=//*[@id="identifierId"]', timeout=timeout)
                        botao_proxima = pagina.locator('xpath=//*[@id="identifierNext"]/div/button/span')
                        pagina.keyboard.insert_text(email_entrada)
                        botao_proxima.click()
                        return True
                    except:
                        print(f'Tentativa [{i}] - Não foi possível logar na plataforma')
                        pagina.wait_for_timeout(1000)
                return False

# --------------------------------------------------------------------

# --------------------------------------------------------------------

            def clicar_em_executar(pagina, tentativas=10, timeout=2000):
                botao_executar = pagina.locator('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[2]/div')
                botao_cancelar = pagina.locator('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[4]/div/cfc-progress-button')
                pagina.wait_for_selector('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[2]/div', timeout=120000)
                for i in range(tentativas):
                    try:
                        botao_executar.click()
                        pagina.wait_for_timeout(2000)
                        botao_cancelar.wait_for(state='visible', timeout=timeout)
                        return True
                    except:
                        print(f'Tentativa [{i}] - Não foi possível executar a consulta SQL')

                        # Pode não executar - Dumpar raise no log de erro
                return False
            
            def acompanhar_execucao(pagina):
                try:
                    botao_salvar_resultados = pagina.locator('xpath=//*[@id="_0rif_save-results-menu-button"]/span[1]')
                    botao_salvar_resultados.wait_for(state='visible', timeout=1800000)
                    return True
                except:
                    print('Não foi possível encontrar o botão "Salvar Resultados"')
                return False

            def click_salvar_result(pagina, tentativas=10, timeout=2000):
                botao_salvar_resultados = pagina.locator('xpath=//*[@id="_0rif_save-results-menu-button"]/span[1]')
                botao_salvar_csv_gdrive = pagina.get_by_role("menuitem", name="CSV (Google Drive) . Salve at")
                for i in range(tentativas):
                    try:
                        botao_salvar_resultados.click()
                        pagina.wait_for_timeout(1000)
                        botao_salvar_csv_gdrive.click()
                        return True
                    except:
                        print(f'Tentativa {i} - Não encontrou o botão "CSV (Google Drive)"')
                return False

            def nova_aba_gdrive(pagina, tentativas=10):
                for i in range(tentativas):
                    try:
                        with pagina.expect_popup() as pagina1_inform:
                            pagina.get_by_role('button', name='Acesse o Google Drive.').click()
                        pagina1 = pagina1_inform.value
                        break
                    except:
                        print(f'Tentativa [{i}] - Não foi possível acessar o Google Drive')

                for i in range(tentativas):
                    try:
                        with pagina1.expect_download() as download_inform:
                            try:
                                pagina1.get_by_label('Fazer o download').click()
                            except:
                                pass
                        print('solicitou download - fora do "with expect_download"')
                        download = download_inform.value
                        download.save_as(caminho_download_temp)
                        print('salvou no caminho - após o "save_as(caminho download)"')
                        break
                    except:
                        print(f'Tentativa [{i}] - Não foi possível acessar o botão "Fazer o download"')
                for i in range(tentativas):  
                    try:
                        shutil.move(caminho_download_temp, caminho_download_final)
                        break
                    except:
                        print(f'Tentativa [{i}] - Não foi possível salvar o arquivo {nome_arq}.')
                


            pagina.goto(link)

            if inserir_email(pagina):
                print('Email inserido.')
            else:
                print('Erro ao inserir email')

            if clicar_em_executar(pagina):
                print('Consulta executada')
            else:
                print('Erro ao executar a consulta')

            if acompanhar_execucao(pagina):
                pass
            else:
                print('Erro de execução')

            if click_salvar_result(pagina):
                print('Botão "Salvar Resultados" pressionado')
            else:
                print('Não foi possível acessar o botão "Salvar Resultados"')


            nova_aba_gdrive(pagina)




            #Inserir pelo CTRL+V:

            
            # Executar query:
 

            # Verificar status de erro...


            # Download dos dados em .csv





            pagina.close()

        print(f'[{threading.current_thread().name}] {id_tarefa} concluída.')


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
