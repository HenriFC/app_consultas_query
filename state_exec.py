class EstadoPrograma:
    def __init__(self):
        self.status = 'Parado'

    def define_status(self, novo_status):
        self.status = novo_status

    def obtem_status(self):
        return self.status

# Instância global de EstadoPrograma
estado_programa = EstadoPrograma()
