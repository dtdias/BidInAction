from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from interface_ui import Ui_interface
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

import threading
import time

class Janela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_interface()
        self.ui.setupUi(self)

        # --- Cria o driver só uma vez ---
        options = Options()
        # options.add_argument("--headless")  # descomente para rodar sem abrir janela
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://vitrinedejoias.caixa.gov.br/Paginas/default.aspx")
        time.sleep(0.5)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Buscar joias").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "buscaVitrine").click()
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "passo").click()
        time.sleep(0.5)

        # Conecta eventos
        self.ui.comboBox.currentTextChanged.connect(self.ao_mudar_uf)
        self.ui.comboBox_2.currentTextChanged.connect(self.ao_mudar_cidade)
        self.ui.comboBox_4.currentTextChanged.connect(self.ao_mudar_periodo)
        self.ui.comboBox_5.currentTextChanged.connect(self.ao_mudar_valor)
        self.ui.pushButton.clicked.connect(self.ao_clicar_botao)

         # lineEdit
        # self.ui.pushButton
        # Dispara o carregamento inicial em thread
        threading.Thread(target=self.carregar_opcoes_site, daemon=True).start()

    def carregar_opcoes_site(self):
        ufs     = self.extrair_opcoes_vitrine('uf')
        valores = self.extrair_opcoes_vitrine('valor')
        cidades = self.extrair_opcoes_vitrine('cidade')
        periodo = self.extrair_opcoes_vitrine('periodoBusca')


        if ufs:
            self.ui.comboBox.addItems(ufs)
        if valores:
            self.ui.comboBox_5.addItems(valores)
        if cidades:
            self.ui.comboBox_2.addItems(cidades)
        if periodo:
            self.ui.comboBox_4.addItems(periodo)

    def extrair_opcoes_vitrine(self, tipo):
        # Seleciona o elemento certo de acordo com o tipo
        select = {
            'uf':     self.driver.find_element(By.ID, "uf"),
            'valor':  self.driver.find_element(By.ID, "valorVenda"),
            'cidade': self.driver.find_element(By.ID, "cidadeVitrine"),
            'periodoBusca': self.driver.find_element(By.ID, 'periodoBusca'),
        }[tipo]

        return [
            opt.text.strip()
            for opt in select.find_elements(By.TAG_NAME, "option")
            if opt.text.strip()
        ]

    def ao_clicar_botao(self):
        text = self.ui.lineEdit.text().strip()
        if not text:
            return
        threading.Thread(
            target=self.enviar_informacoes,
            args=(text,),
            daemon=True
        ).start()

    def ao_mudar_uf(self, uf_texto):
        if not uf_texto:
            return
        threading.Thread(
            target=self.carregar_conteudo_para_uf,
            args=(uf_texto,),
            daemon=True
        ).start()

    def ao_mudar_cidade(self, cidade_texto):
        if not cidade_texto:
            return
        threading.Thread(
            target=self.carregar_conteudo_para_cidades,
            args=(cidade_texto,),
            daemon=True
        ).start()

    def ao_mudar_periodo(self, periodo_texto):
        if not periodo_texto:
            return
        threading.Thread(
            target=self.carregar_conteudo_para_periodos,
            args=(periodo_texto,),
            daemon=True
        ).start()

    def ao_mudar_valor(self, valor_texto):
        if not valor_texto:
            return
        threading.Thread(
            target=self.carregar_conteudo_para_valores,
            args=(valor_texto,),
            daemon=True
        ).start()

    def enviar_informacoes(self, text:str):
        try:
            # 1) encontra o input
            elem = self.driver.find_element(By.ID, "loteContrato")
            # 2) limpa e envia o texto
            elem.clear()
            elem.send_keys(text)
            # 3) dispara os eventos JS para o site “ver” a mudança
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input'));"
                "arguments[0].dispatchEvent(new Event('change'));",
                elem
            )
            time.sleep(1)
            self.driver.find_element(By.NAME, "passo").click()


        except Exception as e:
            print("Erro ao escrever no loteContrato:", e) 

    def carregar_conteudo_para_uf(self, uf_texto):
        try:
            print(f"[INFO] Selecionando UF: {uf_texto}")
            uf_element = self.driver.find_element(By.ID, "uf")
            # Dispara o evento de mudança para atualizar a lista de cidades
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                uf_element, uf_texto
            )
            time.sleep(0.5)
            # Após a mudança, recarrega as cidades
            novas = self.extrair_opcoes_vitrine('cidade')
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(novas)
        except Exception as e:
            print("Erro ao selecionar UF:", e)

    def carregar_conteudo_para_cidades(self, cidade_texto):
        try:
            print(f"[INFO] Selecionando Cidade: {cidade_texto}")
            # Cria o Select a partir do <select id="cidadeVitrine">
            select_city = Select(self.driver.find_element(By.ID, "cidadeVitrine"))
            # Seleciona pela opção visível
            select_city.select_by_visible_text(cidade_texto)

            # Aguarda o carregamento das opções de período (até 10s)
            WebDriverWait(self.driver, 10).until(
                lambda d: len(self.extrair_opcoes_vitrine('periodoBusca')) > 1
            )

            # Reextrai e popula no comboBox_4
            periodos = self.extrair_opcoes_vitrine('periodoBusca')
            self.ui.comboBox_4.clear()
            self.ui.comboBox_4.addItems(periodos)

        except Exception as e:
            print("Erro ao selecionar CIDADE:", e)

    def carregar_conteudo_para_periodos(self, periodo_texto):
        try:
            print(f"[INFO] Selecionando PERIODO: {periodo_texto}")
            # Cria o Select a partir do <select id="cidadeVitrine">
            select_periodo = Select(self.driver.find_element(By.ID, "periodoBusca"))
            # Seleciona pela opção visível
            select_periodo.select_by_visible_text(periodo_texto)

        except Exception as e:
            print("Erro ao selecionar PERIODO:", e)
    
    def carregar_conteudo_para_valores(self, valores_texto):
        try:
            print(f"[INFO] Selecionando VALOR: {valores_texto}")
            # Cria o Select a partir do <select id="cidadeVitrine">
            select_periodo = Select(self.driver.find_element(By.ID, "valorVenda"))
            # Seleciona pela opção visível
            select_periodo.select_by_visible_text(valores_texto)

        except Exception as e:
            print("Erro ao selecionar VALOR:", e)


if __name__ == "__main__":
    app = QApplication([])
    janela = Janela()
    janela.show()
    app.exec()
