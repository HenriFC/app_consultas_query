from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


import multiprocessing      # Realizar multitarefas 

def iniciar_edge():

    options = EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)

    # Instânciando a janela do navegador:
    navegador_edge = webdriver.Edge(options=options)
    navegador_edge.minimize_window()
    # Acessando o link:
    navegador_edge.get("https://www.google.com/")

    # Digitando um texto no campo e apertando enter:
    navegador_edge.find_element('xpath', '//*[@id="APjFqb"]').send_keys('Vasco da Gama' + Keys.ENTER)

