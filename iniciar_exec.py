import os
import json
import shutil
import tempfile
import threading
import time
from pyautogui import press
from playwright.sync_api import sync_playwright
from datetime import date, datetime
from cronograma_geral import obter_cronograma_status
from state_exec import estado_programa, estado_database



PASTA_LOGS = 'logs_exec_tarefas\\'
PASTA_DOWNLOAD_TEMP = 'downloads_temp\\'
CAMINHO_ARQ = 'database_cronograma.json'
CAMINHO_DB_EMAIL = 'database_email.json'


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
                                caminho_salvar_arq = detal['CAMINHO_SALVAR']
                                email_entrada = obter_email()
                                link = detal['QUERY']
                                # Inicia essa tarefa:
                                self.iniciar_tarefa(id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, caminho_salvar_arq, email_entrada, link)
                            else:
                                self.base_atualizada.append(extracao[item])
                        for i in range(10):
                            try:
                                json.dump(self.base_atualizada, file_temp,indent=4, ensure_ascii=False)
                                break
                            except:
                                time.sleep(1)
                        press('shift')
                    shutil.move(file_temp.name, CAMINHO_ARQ)
                    time.sleep(1)
                    obter_cronograma_status()
                    

                        
            time.sleep(1)  # Aguarda antes de verificar novamente

    def iniciar_tarefa(self, id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, caminho_salvar_arq, email_entrada, link):
        # Inicia uma nova tarefa em uma thread separada
        thread_tarefa = threading.Thread(target=self.executar_tarefa, args=(id_tarefa, nome_arq, caminho_salvar_arq, email_entrada, link))
        thread_tarefa.start()
        self.threads_tarefas.append(thread_tarefa)

    def executar_tarefa(self, id_tarefa, hr_ini_consulta, hr_fim_consulta, nome_arq, caminho_salvar_arq, email_entrada, link):
        print(f'[{threading.current_thread().name}] {id_tarefa} iniciada.')

        ARQ_LOG_TAREFA = PASTA_LOGS + id_tarefa + '.json'
        
        def criar_log_execucao():
            try:
                with open(ARQ_LOG_TAREFA, 'r', encoding='utf-8') as criando_log:
                    pass
            except FileNotFoundError:
                with open(ARQ_LOG_TAREFA, 'w', encoding='utf-8') as criando_log:
                    dados_novos = {
                        "HORA_INICIO_PLAN": "__:__:__",
                        "DATA_INICIO_CONS": "__.__.__",
                        "HORA_INICIO_CONS": "__:__:__",
                        "ATRASO": "__:__:__",
                        "DATA_FIM_CONS": "__.__.__",
                        "HORA_FIM_CONS": "__:__:__",
                        "TEMPO_EXEC": "__:__:__",
                        "STATUS": "Executando",
                        "OBSERVAÇÃO": ""
                    }
                    json.dump(dados_novos, criando_log, indent=4, ensure_ascii=False)
        
        def atualizar_log_execucao(reg1, valor1, reg2=None, valor2=None, reg3=None, valor3=None, reg4=None, valor4=None):
            with open(ARQ_LOG_TAREFA, 'r', encoding='utf-8') as dados_log, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
                novos_dados = json.load(dados_log)
                novos_dados[reg1] = valor1
                novos_dados[reg2] = valor2
                novos_dados[reg3] = valor3
                novos_dados[reg4] = valor4
                json.dump(novos_dados, file_temp, indent=4, ensure_ascii=False)
            shutil.move(file_temp.name, ARQ_LOG_TAREFA)
            time.sleep(1)

        criar_log_execucao()
        try:
            with sync_playwright() as pw:
                navegador = pw.chromium.launch(channel='msedge', headless=False)
                pagina = navegador.new_page()
                caminho_download_temp = os.path.join(PASTA_DOWNLOAD_TEMP, nome_arq)
                caminho_download_final = os.path.join(caminho_salvar_arq, nome_arq)

                def inserir_email(pagina, tentativas=10, timeout=2000):
                    atualizar_log_execucao('OBSERVAÇÃO', 'Realizando login')
                    estado_database.define_status_database('Modificada')
                    try:
                        pagina.wait_for_selector('xpath=//*[@id="identifierId"]', timeout=120000)
                        print('encerrou a espera pelo campo "email"')
                        pagina.wait_for_selector('xpath=//*[@id="identifierNext"]/div/button/span', timeout=120000)
                        print('encerrou a espera pelo botão "Próximo"')
                    except:
                        return False
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

                def clicar_em_executar(pagina, tentativas=10):
                    try:
                        botao_executar = pagina.locator('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[2]/div')
                        pagina.wait_for_selector('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[2]/div', timeout=120000)
                    except:
                        return False

                    for i in range(tentativas):
                        try:
                            botao_executar.click()
                            global data_inicio
                            global hora_inicio
                            data_inicio = date.today().strftime('%d.%m.%Y')
                            hora_inicio = datetime.now().strftime('%H:%M:%S')
                            atualizar_log_execucao('DATA_INICIO_CONS', data_inicio, 'HORA_INICIO_PLAN', hora_inicio, 'OBSERVAÇÃO', 'Botão "Executar" pressionado. Aguardando início')
                            estado_database.define_status_database('Modificada')
                            return True
                        except:
                            print(f'Tentativa [{i}] - Não foi possível executar a consulta SQL')
                    return False

                def acompanhar_execucao(pagina):
                    try:
                        botao_cancelar = pagina.locator('xpath=//*[@id="_0rif_shared-query-editor-action-bar-bqui-1"]/mat-toolbar/div[3]/div/div/div[1]/cfc-action-bar-content-wrapper[4]/div/cfc-progress-button')
                        botao_salvar_resultados = pagina.locator('xpath=//*[@id="_0rif_save-results-menu-button"]/span[1]')
                    except:
                        return False
                    
                    try:
                        botao_cancelar.wait_for(state='visible', timeout=1800000)
                        global data_final
                        global hora_final
                        data_final = date.today().strftime('%d.%m.%Y')
                        hora_final = datetime.now().strftime('%H:%M:%S')

                        atraso_decorrido_str = f"{data_inicio} {hora_inicio}"
                        atraso_decorrido = datetime.now() - datetime.strptime(atraso_decorrido_str, '%d.%m.%Y %H:%M:%S')
                        total_segundos = int(atraso_decorrido.total_seconds())
                        horas, resto = divmod(total_segundos, 3600)
                        minutos, segundos = divmod(resto, 60)
                        atraso_decorrido = f'{horas:02}:{minutos:02}:{segundos:02}'

                        
                        atualizar_log_execucao('DATA_INICIO_CONS', data_final, 'HORA_INICIO_CONS', hora_final, 'ATRASO', atraso_decorrido, 'OBSERVAÇÃO', 'Consulta em execução')
                        estado_database.define_status_database('Modificada')
                        botao_salvar_resultados.wait_for(state='visible', timeout=1800000)
                        return True
                    except:
                        print('Não foi possível encontrar o botão "Salvar Resultados". A consulta falhou.')
                    return False

                def click_salvar_result(pagina, tentativas=10, timeout=2000):
                    try:
                        botao_salvar_resultados = pagina.locator('xpath=//*[@id="_0rif_save-results-menu-button"]/span[1]')
                        botao_salvar_csv_gdrive = pagina.get_by_role("menuitem", name="CSV (Google Drive) . Salve at")
                    except:
                        return False
                    for i in range(tentativas):
                        try:
                            botao_salvar_resultados.click()
                            data_atual = date.today().strftime('%d.%m.%Y')
                            hora_atual = datetime.now().strftime('%H:%M:%S')

                            tempo_exec_str = f"{data_final} {hora_final}"
                            tempo_exec = datetime.now() - datetime.strptime(tempo_exec_str, '%d.%m.%Y %H:%M:%S')
                            total_segundos = int(tempo_exec.total_seconds())
                            horas, resto = divmod(total_segundos, 3600)
                            minutos, segundos = divmod(resto, 60)
                            tempo_exec = f'{horas:02}:{minutos:02}:{segundos:02}'
                            
                            atualizar_log_execucao('DATA_FIM_CONS', data_atual, 'HORA_FIM_CONS', hora_atual, 'TEMPO_EXEC', tempo_exec, 'OBSERVAÇÃO', 'Exportando arquivo')
                            estado_database.define_status_database('Modificada')
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
                            atualizar_log_execucao( 'STATUS', 'Finalizado', 'OBSERVAÇÃO', 'Finalizado')
                            estado_database.define_status_database('Modificada')
                            break
                        except:
                            print(f'Tentativa [{i}] - Não foi possível salvar o arquivo {nome_arq}.')

                    
                # Início da execução

                pagina.goto(link)

                if inserir_email(pagina):
                    print('Email inserido.')
                else:
                    atualizar_log_execucao( 'STATUS', 'Finalizado', 'OBSERVAÇÃO', 'Erro: Impossível inserir e-mail')
                    estado_database.define_status_database('Modificada')
                    print('Erro ao inserir email')
                    pagina.close()

                if clicar_em_executar(pagina):
                    print('Consulta executada')
                else:
                    print('Erro ao executar a consulta')
                    atualizar_log_execucao( 'STATUS', 'Finalizado', 'OBSERVAÇÃO', 'Erro: Impossível acessar a plataforma')
                    estado_database.define_status_database('Modificada')
                    pagina.close()

                if acompanhar_execucao(pagina):
                    pass
                else:
                    print('Erro de execução')
                    atualizar_log_execucao( 'STATUS', 'Finalizado', 'OBSERVAÇÃO', 'Erro: Consulta não finalizada')
                    estado_database.define_status_database('Modificada')

                if click_salvar_result(pagina):
                    print('Botão "Salvar Resultados" pressionado')
                else:
                    print('Não foi possível acessar o botão "Salvar Resultados"')
                    atualizar_log_execucao( 'STATUS', 'Finalizado', 'OBSERVAÇÃO', 'Erro: Impossível acessar Google Drive')
                    estado_database.define_status_database('Modificada')


                nova_aba_gdrive(pagina)


                pagina.close()

            print(f'[{threading.current_thread().name}] {id_tarefa} concluída.')
        except:
            pass

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
