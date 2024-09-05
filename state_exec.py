class EstadoPrograma:
    # Receberá doi status: Parado ou Executando
    def __init__(self):
        self.status = 'Inicio'

    def define_status(self, novo_status):
        self.status = novo_status

    def obtem_status(self):
        return self.status

class EstadoBase:
    # Receberá dois status distintos: Modificada ou Não modificada
    def __init__(self):
        self.status_database = 'Inicio'

    def define_status_database(self, novo_status_database):
        self.status_database = novo_status_database

    def obtem_status_database(self):
        return self.status_database
# Instância global de EstadoPrograma

estado_programa = EstadoPrograma()
estado_database = EstadoBase()
