import json
import shutil
import tempfile
from os import remove
from datetime import date, datetime, timedelta
from state_exec import estado_database
CAMINHO_DB_JSON = 'db_folder\\database.json'
CAMINHO_HIST_CRONO = 'db_folder\\database_cronograma.json'
PASTA_LOGS = 'db_folder\\logs_exec_tarefas\\'

# Criar JSON com o fluxo de execuções em ordem cronológica. Esse arquivo será utilizado para mapear quais processos serão, ou foram executados
def obter_cronograma_status():
    aux_indice_horario = 0
    
    with open(CAMINHO_HIST_CRONO, 'r', encoding='utf-8') as crono_file, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
        extracao = json.load(crono_file)
        registros_atualizados = []
        for i in range(len(extracao)):
            if extracao[i]['STATUS'] in ('Executando', 'Finalizado'):
                arq_log_exec = extracao[i]['ID'] + '.json'

                try:
                    with open(PASTA_LOGS + arq_log_exec, 'r', encoding='utf-8') as temp_log:
                        log_extraido = json.load(temp_log)
                        extracao[i]['HORA_INICIO_PLAN'] = log_extraido['HORA_INICIO_PLAN']
                        extracao[i]['DATA_INICIO_CONS'] = log_extraido['DATA_INICIO_CONS']
                        extracao[i]['HORA_INICIO_CONS'] = log_extraido['HORA_INICIO_CONS']
                        extracao[i]['ATRASO'] = log_extraido['ATRASO']
                        extracao[i]['DATA_FIM_CONS'] = log_extraido['DATA_FIM_CONS']
                        extracao[i]['HORA_FIM_CONS'] = log_extraido['HORA_FIM_CONS']
                        extracao[i]['TEMPO_EXEC'] = log_extraido['TEMPO_EXEC']
                        extracao[i]['STATUS'] = log_extraido['STATUS']
                        extracao[i]['OBSERVAÇÃO'] = log_extraido['OBSERVAÇÃO']
                        registros_atualizados.append(extracao[i])
                    if extracao[i]['STATUS'] == 'Finalizado':
                        remove(PASTA_LOGS + arq_log_exec)
                except FileNotFoundError:
                    registros_atualizados.append(extracao[i])
            else:
                registros_atualizados.append(extracao[i])
            
        json.dump(registros_atualizados, file_temp, indent=4, ensure_ascii=False)
    shutil.move(file_temp.name, CAMINHO_HIST_CRONO)

    try:
        # Remover tarefas não iniciadas com data futura.
        with open(CAMINHO_HIST_CRONO, 'r', encoding='utf-8') as crono_file:
            crono_temp = json.load(crono_file)
            crono_temp = [y for y in crono_temp if y["STATUS"] != "Pendente"]
    except FileNotFoundError:
        crono_temp = []

    with open(CAMINHO_DB_JSON, 'r', encoding='utf-8') as base_dados, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
        extracao = json.load(base_dados)
        novos_registros = []

        for key, value in extracao.items():
            while aux_indice_horario <= 11:
                data_atual = date.today().strftime('%d.%m.%Y')
                horario = value["horario"][aux_indice_horario]
                if horario == '':
                    break
                horario_base_convert = datetime.strptime(f"{data_atual} {horario}", '%d.%m.%Y %H:%M')
                horario_agora_convert = datetime.strptime(f"{data_atual} {datetime.now().strftime('%H:%M')}", '%d.%m.%Y %H:%M')
                if horario_base_convert < horario_agora_convert:
                    horario_base_convert += timedelta(days=1)
                    data_atual = horario_base_convert.strftime('%d.%m.%Y')
                if horario_base_convert == horario_agora_convert:
                    id = f"{data_atual}.{horario[:2]}.{horario[3:5]}.{key}"
                    registro_crono = {
                        "ID": id,
                        "ATIVIDADE": key,
                        "DATA": data_atual,
                        "HORA_INICIO_PLAN": horario + ':00',
                        "DATA_INICIO_CONS": "__.__.__",
                        "HORA_INICIO_CONS": "__:__:__",
                        "ATRASO": "__:__:__",
                        "DATA_FIM_CONS": "__.__.__",
                        "HORA_FIM_CONS": "__:__:__",
                        "TEMPO_EXEC": "__:__:__",
                        "NOME_ARQUIVO": value["nome"],
                        "STATUS": "Pendente",
                        "OBSERVAÇÃO": "-",
                        "QUERY": value["query"],
                        "CAMINHO_SALVAR": value["caminho_salvar"]
                    }

                    # Verificar se o registro já existe no cronograma
                    if any(item["ID"] == id for item in crono_temp):
                        pass  # Já registrado, não precisa adicionar
                    else:
                        novos_registros.append(registro_crono)
                    horario_base_convert += timedelta(days=1)
                    data_atual = horario_base_convert.strftime('%d.%m.%Y')
                    
                # Criar ID único baseado na data e horário
                id = f"{data_atual}.{horario[:2]}.{horario[3:5]}.{key}"
                registro_crono = {
                    "ID": id,
                    "ATIVIDADE": key,
                    "DATA": data_atual,
                    "HORA_INICIO_PLAN": horario + ':00',
                    "DATA_INICIO_CONS": "__.__.__",
                    "HORA_INICIO_CONS": "__:__:__",
                    "ATRASO": "__:__:__",
                    "DATA_FIM_CONS": "__.__.__",
                    "HORA_FIM_CONS": "__:__:__",
                    "TEMPO_EXEC": "__:__:__",
                    "NOME_ARQUIVO": value["nome"],
                    "STATUS": "Pendente",
                    "OBSERVAÇÃO": "-",
                    "QUERY": value["query"],
                    "CAMINHO_SALVAR": value["caminho_salvar"]
                }

                # Verificar se o registro já existe no cronograma
                if any(item["ID"] == id for item in crono_temp):
                    pass  # Já registrado, não precisa adicionar
                else:
                    novos_registros.append(registro_crono)
        
                aux_indice_horario += 1

            aux_indice_horario = 0

        # Adicionar novos registros ao cronograma
        crono_temp.extend(novos_registros)
        json.dump(crono_temp, file_temp, indent=4, ensure_ascii=False)
    shutil.move(file_temp.name, CAMINHO_HIST_CRONO)
    estado_database.define_status_database('Modificada')

