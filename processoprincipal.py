import json
import shutil
import tempfile
from datetime import date

caminho_db_json2 = 'database.json'
caminho_hist_crono = 'database_cronograma.json'

# Criar JSON com o fluxo de execuções em ordem cronológica. Esse arquivo será utilizado para mapear quais processos serão 
def obter_cronograma_status():
    data_atual = (date.today()).strftime('%d.%m.%Y')
    print(data_atual)
    aux_indice_horario = 0
    aux_indice_base = 0
    id = ''
    ativ = ''
    arq = ''
    hor_ini = ''
    hor_fim = ''
    stat = ''
    obs = ''

    try:
        crono_temp = json.load(caminho_hist_crono)
    except:
        crono_temp = {}

    
    registro_crono = {}
    with open(caminho_db_json2, 'r', encoding='utf-8') as arquivojs, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as file_temp:
        extracao = json.load(arquivojs)
        validar = {}
        for x in extracao.items():
            while aux_indice_horario <= 11:
                if x[1]['horario'][aux_indice_horario] == '':
                    break
                id = f"{data_atual}.{x[1]['horario'][aux_indice_horario][:2]}.{x[1]['horario'][aux_indice_horario][3:5]}.{x[0]}"
                ativ = x[0]
                hor_ini = x[1]['horario'][aux_indice_horario]
                hor_fim = "__:__"
                arq = x[1]['nome']
                stat = "Pendente"
                obs = "-"
                registro_crono = {                    
                    "ID": id,
                    "ATIVIDADE": ativ,
                    "HORA INICIO": hor_ini,
                    "HORA FIM": hor_fim,
                    "NOME ARQUIVO": arq,
                    "STATUS": stat,
                    "OBSERVAÇÃO": obs
                    }

                if registro_crono['ID'] in crono_temp:
                    pass
                else:
                    validar.update(registro_crono)

                

            
                aux_indice_horario += 1
            print(validar)
            print('ASASASAASS')
            aux_indice_horario = 0
            aux_indice_base += 1


        print('****************************************')

obter_cronograma_status()     
