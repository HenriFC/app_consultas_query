import os
import json
import shutil
import tempfile
import threading
from datetime import date, datetime, timedelta
from time import sleep
from state_exec import estado_programa

pasta_logs = 'logs_exec'
caminho_arq = 'database_cronograma.json'


class ControlarExecucao():
    def __init__(self):
        self.threads = []
        self.executando = False
        self.lock = threading.Lock()
        self.verificar_tarefas()

    def iniciar_tarefa(self):
        # Cria o log em TXT para salvar os status

        # realiza toda a execução dos comandos.


        pass

    # Atualizar o arquivo com os logs de execução
    def atualizar_database(self):

        pass

    # Verificar se há tarefa a ser executada no horário atual (Utilizar o STATUS como parâmetro?)
    def verificar_tarefas(self):
        print(caminho_arq)
        with open(caminho_arq, 'r', encoding='utf-8') as crono_original, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
            extracao = json.load(crono_original)
            if estado_programa.obtem_status() == "Executando":
                for item, detal in enumerate(extracao):
                    print(detal['ID'])
                    sleep(1)

  

        pass


# Função que obtem as tarefas de um arquivo json.
# A finalidade é tanto obter as tarefas como atualizá-las com novas tarefas ao longo do tempo.



# Função que obtém a lista atual de tarefas e faz o start da mesma caso esteja no horário programado