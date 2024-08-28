import json
import shutil
import tempfile

caminho_db_json2 = 'database.json'

# Criar JSON com o fluxo de execuções em ordem cronológica. Esse arquivo será utilizado para mapear quais processos serão 
def obter_cronograma():
    aux_indice_horario = 0
    lista_cronograma = ''
    with open(caminho_db_json2, 'r', encoding='utf-8') as arquivojs, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as crono_temp:
        extracao = json.load(arquivojs)
        for x in extracao.items():
            while aux_indice_horario <= 11:
                if x[1]['horario'][aux_indice_horario] == '':
                    break
                print('ATIVIDADE: ', x[0],'horário: ', x[1]['horario'][aux_indice_horario])
                aux_indice_horario += 1
            aux_indice_horario = 0
        print('****************************************')

