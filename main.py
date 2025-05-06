from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from interface_ui import Ui_interface
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time

class Janela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_interface()
        self.ui.setupUi(self)

        self.driver = None
        self.opcoes_cidade_atuais = []  # Armazena última versão das cidades

        # Conecta eventos
        self.ui.comboBox.currentTextChanged.connect(self.ao_mudar_uf)

        # Inicia Selenium e monitoramento em paralelo
        threading.Thread(target=self.carregar_opcoes_site, daemon=True).start()

    def carregar_opcoes_site(self):
        ufs = self.extrair_opcoes_vitrine()
        if ufs:
            self.ui.comboBox.addItems(ufs)

        # Inicia monitoramento contínuo das cidades
        threading.Thread(target=self.monitorar_cidades, daemon=True).start()

    def extrair_opcoes_vitrine(self):
        try:
            options = Options()
            self.driver = webdriver.Chrome(options=options)

            self.driver.get("https://vitrinedejoias.caixa.gov.br/Paginas/default.aspx")
            time.sleep(0.3)

            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Buscar joias").click()
            time.sleep(0.3)

            self.driver.find_element(By.ID, "buscaVitrine").click()
            time.sleep(0.3)

            self.driver.find_element(By.NAME, "passo").click()
            time.sleep(0.3)

            select_uf = self.driver.find_element(By.ID, "uf")
            opcoes_uf = [
                option.text.strip()
                for option in select_uf.find_elements(By.TAG_NAME, "option")
                if option.text.strip()
            ]

        
            return opcoes_uf

        except Exception as e:
            print("Erro com Selenium:", e)
            return []

    def ao_mudar_uf(self, uf_texto):
        if not self.driver or not uf_texto:
            return
        threading.Thread(target=self.carregar_cidades_para_uf, args=(uf_texto,), daemon=True).start()

    def carregar_cidades_para_uf(self, uf_texto):
        try:
            print(f"[INFO] Selecionando UF: {uf_texto}")
            uf_element = self.driver.find_element(By.ID, "uf")
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                uf_element, uf_texto
            )

        except Exception as e:
            print("Erro ao selecionar UF:", e)

    def monitorar_cidades(self):
        while True:
            try:
                if not self.driver:
                    time.sleep(1)
                    continue

                select_cidade = self.driver.find_element(By.NAME, "cidadeVitrine")
                novas_opcoes = [
                    option.text.strip()
                    for option in select_cidade.find_elements(By.TAG_NAME, "option")
                    if option.text.strip()
                ]

                if novas_opcoes and novas_opcoes != self.opcoes_cidade_atuais:
                    print("[INFO] Novas cidades detectadas:", novas_opcoes)
                    self.opcoes_cidade_atuais = novas_opcoes.copy()

                    def atualizar(lista=novas_opcoes):
                        self.ui.comboBox_2.clear()
                        self.ui.comboBox_2.addItems(lista)


                    QTimer.singleShot(0, atualizar)

            except Exception as e:
                print("Erro ao monitorar cidades:", e)

            time.sleep(0.5)  # Verifica a cada 0.5 segundo

if __name__ == "__main__":
    app = QApplication([])
    janela = Janela()
    janela.show()
    app.exec()
