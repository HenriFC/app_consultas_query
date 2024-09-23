import json
import shutil
import tempfile
from datetime import date, datetime, timedelta
from state_exec import estado_database
CAMINHO_DB_JSON = 'database.json'
CAMINHO_HIST_CRONO = 'database_cronograma.json'

# Criar JSON com o fluxo de execuções em ordem cronológica. Esse arquivo será utilizado para mapear quais processos serão, ou foram executados
def obter_cronograma_status():
    aux_indice_horario = 0

    # Carregar o cronograma existente ou iniciar um novo
    try:
        # Remover tarefas não iniciadas com data futura. Tarefas não iniciadas
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
                horario_validador = datetime.strptime(f"{data_atual} {horario}:59", '%d.%m.%Y %H:%M:%S')
                print(horario_validador, datetime.now())
                if horario_validador < datetime.now():
                    horario_validador += timedelta(days=1)
                    data_atual = horario_validador.strftime('%d.%m.%Y')

                # Criar ID único baseado na data e horário
                id = f"{data_atual}.{horario[:2]}.{horario[3:5]}.{key}"
                registro_crono = {
                    "ID": id,
                    "ATIVIDADE": key,
                    "DATA": data_atual,
                    "HORA_INICIO_PLAN": horario + ':00',
                    "HORA_INICIO_CONS": "__:__:__",
                    "ATRASO": "__:__:__",
                    "HORA_FIM_CONS": "__:__:__",
                    "TEMPO_EXEC": "__:__:__",
                    "NOME_ARQUIVO": value["nome"],
                    "STATUS": "Pendente",
                    "OBSERVAÇÃO": "-",
                    "QUERY": value["query"]
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

    # Salvar o cronograma atualizado



