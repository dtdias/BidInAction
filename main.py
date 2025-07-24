from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from interface_ui import Ui_interface
from resultado import Ui_interface as ResultadoUi
from PySide6.QtWebEngineWidgets import QWebEngineView
import tempfile, os
# from bs4 import BeautifulSoup
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
        # if not text:
            # return
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
            elem = self.driver.find_element(By.ID, "loteContrato")
            if text:
                elem.clear()
                elem.send_keys(text)            
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new Event('input'));"
                    "arguments[0].dispatchEvent(new Event('change'));",
                    elem
                )
            time.sleep(0.5)
            self.driver.find_element(By.ID, "passo2Vitrine").click()

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

    class ResultadoJanela(QMainWindow):
        def __init__(self, html_content):
            super().__init__()
            self.ui = ResultadoUi()
            self.ui.setupUi(self)

            # Salva HTML temporário
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
            temp.write(html_content)
            temp.close()

            self.ui.webEngineView.load(f"file:///{temp.name.replace(os.sep, '/')}")
            self.temp_file = temp.name

            self.ui.pushButton.clicked.connect(self.close)       # VOLTAR
            self.ui.pushButton_2.clicked.connect(self.close)     # SAIR

        def closeEvent(self, event):
            try:
                os.remove(self.temp_file)
            except:
                pass
            super().closeEvent(event)
        
class SearchWindow(QMainWindow):
    fontMedium = QFont()
    fontDefault = QFont()
    requester = Requester()
    city_by_uf: dict[str,list[dict]] = dict()
    bid_period_by_city: dict[str,list[dict]] = dict()
    
    
    def __init__(self):
        super().__init__()
 
        self.main_view = QWidget()
        self.main_layout = QVBoxLayout(self.main_view)
        self.resize(650, 500)
        self.setMaximumSize(QSize(650, 500))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setWindowTitle(u"BUSCADOR DE LEIL\u00d5ES DE JOIAS DA CAIXA")
        self.setCentralWidget(self.main_view)
        self.initialize_fonts()
 
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(12)
        self.main_view.setContentsMargins(QMargins(120,40,120,0))

        
        self.wgTitle = Title(self.main_layout)
        self.wgTitle._label.setFont(self.fontMedium)
        
        self.wgSearchFilter = SearchFilter(self.main_layout)
        
        self.wgPickUpLocation = PickUpLocation(self.main_layout)
        self.wgPickUpLocation._inputUf.addItems(self.requester.request_uf_list())
        
        self.wgPickUpLocation._inputUf.currentTextChanged.connect(self.onChangeUf)
        self.wgPickUpLocation._inputCity.currentTextChanged.connect(self.onChangeCity)
        
        self.wgBidPeriod = BidPeriod(self.main_layout)
        self.wgBidPeriod._label.setFont(self.fontMedium)
        self.wgBidPeriod._input.currentTextChanged.connect(self.onChangeBitPeriod)

    def onChangeUf(self, uf: str):
        self.city_by_uf[uf] = self.requester.request_cities_list(uf)
        self.wgPickUpLocation.reset_inputCity()
        self.wgBidPeriod.reset_periods()
        self.wgPickUpLocation._inputCity.addItems(
            list(map(lambda city: city['nome'], self.city_by_uf[uf]))
        )
    
    def onChangeCity(self, city: str):
        if not city:
            return
        currentUf: str = self.wgPickUpLocation._inputUf.currentText()
        for city_content in self.city_by_uf[currentUf]:
            if str.find(city,city_content['nome']):
                continue
            name = city_content["nome"]
            self.bid_period_by_city[name] = self.requester.request_bid_period(city_content['codigo'])
            self.wgBidPeriod.reset_periods()
            
            self.wgBidPeriod._input.addItems(
                list(map(lambda period: period['periodoDeLance'], self.bid_period_by_city[name]))
            )
            
    def onChangeBitPeriod(self, period: str):
        if not period:
            return
        currentCity: str = self.wgPickUpLocation._inputCity.currentText()
        for period_content in self.bid_period_by_city[currentCity]:
            if period == period_content['periodoDeLance']:
                print(period_content['inicioLance'])
                
    
    def initialize_fonts(self):
        self.fontMedium.setPointSize(12)        
        self.fontDefault.setPointSize(10)
        pass
    
    

if __name__ == "__main__":
    app = QApplication([])
    janela = SearchWindow()
    janela.show()
    sys.exit(app.exec())
