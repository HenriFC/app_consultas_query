import json
import shutil
import tempfile
from app import caminho_db_json

# Criar JSON com o fluxo de execuções em ordem cronológica. Esse arquivo será utilizado para mapear quais processos serão 
def obter_cronograma():
    with open(caminho_db_json, 'r', encoding='utf-8') as arquivojs, tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as crono_temp:
        try:
            dados_temp = json.load(arquivojs)
        except:
            return



