from threading import Thread
from tracemalloc import start
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog)
from PySide6.QtCore import (Qt, QSize,QMargins )
from PySide6.QtGui import (QFont)

from components.bit_period import BidPeriod
from components.pick_up_location import PickUpLocation
from components.search_filter import SearchFilter
from components.title import Title
from components.values_range import ValuesRange
from models.bid_period_model import BidPeriodModel
from models.bid_query_model import BidQueryModel
from services.request_service import RequesterService
from services.storage_service import StorageService
from views.result_window import ResultWindow

class SearchWindow(QMainWindow):
    fontMedium = QFont()
    fontDefault = QFont()
    requester = RequesterService()
    city_by_uf: dict[str,list[dict]] = dict()
    bid_period_by_city: dict[str,list[dict]] = dict()
    storage = StorageService()
    wgSearchFilter: SearchFilter
    wgPickUpLocation: PickUpLocation
    wgBidPeriod: BidPeriod
    wgValuesRange: ValuesRange
    wgSubmitButton: QPushButton
    
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
        self.main_layout.setSpacing(15)
        self.main_view.setContentsMargins(QMargins(100,40,100,0))

        self.wgTitle = Title(self.main_layout)
        self.wgTitle._label.setFont(self.fontMedium)
        
        self.wgSearchFilter = SearchFilter(self.main_layout)
        
        self.wgPickUpLocation = PickUpLocation(self.main_layout)
        self.wgPickUpLocation._label.setFont(self.fontMedium)
        self.wgPickUpLocation._inputUf.addItems([x.acronym for x in self.requester.request_uf_list()])
        
        self.wgPickUpLocation._inputUf.currentTextChanged.connect(lambda o: Thread(target=self.onChangeUf,args=(o,)).start())
        self.wgPickUpLocation._inputCity.currentTextChanged.connect(lambda o: Thread(target=self.onChangeCity, args=(o,)).start())
        
        self.wgBidPeriod = BidPeriod(self.main_layout)
        self.wgBidPeriod._label.setFont(self.fontMedium)

        self.wgValuesRange = ValuesRange(self.main_layout)
        self.wgValuesRange._label.setFont(self.fontMedium)
        self.wgValuesRange._input.addItems(list(self.storage.values_range.keys()))
        
        self.wgSubmitButton = QPushButton(u"Continuar")
        self.wgSubmitButton.clicked.connect(self.onSubmitQuery)
        self.main_layout.addWidget(self.wgSubmitButton)

    def onChangeUf(self, uf: str):
        self.wgPickUpLocation.reset_inputCity()
        self.wgBidPeriod.reset_periods()
        
        cities = self.storage.cities
        if cities.get(uf) == None:
            cities[uf] = {}
            for city in self.requester.request_cities_list(uf):
                if cities[uf].get(city.name) != None: continue
                cities[uf][city.name] = city

        self.wgPickUpLocation._inputCity.addItems(list(cities[uf].keys()))
    
    def onChangeCity(self, city_name: str):
        if not city_name: return
        self.wgBidPeriod.reset_periods()
        
        periods = self.storage.periods
        uf = self.wgPickUpLocation._inputUf.currentText()
        city = self.storage.cities[uf][city_name]
        
        for period in self.requester.request_bid_period(city.code):
            if periods.get(city.name) == None: periods[city.name] = {}
            periods[city.name][period.bid_period] = period

        self.wgBidPeriod._input.addItems(list(periods[city_name].keys()))
                
    def onSubmitQuery(self):
        filter = self.wgSearchFilter._input.text()
        uf = self.wgPickUpLocation._inputUf.currentText()
        if uf == "": return print("Selecione uma UF")
            
        city = self.wgPickUpLocation._inputCity.currentText()
        if city == "": print("Selecione uma cidade")
            
        period = self.wgBidPeriod._input.currentText()
        if period == "": return print("Selecione um período de lance")
        period = self.storage.periods[city][period].start_date

        values_range = self.wgValuesRange._input.currentText()
        if values_range == "": return print("Selecione uma faixa de valor")
        values_range = self.storage.values_range[values_range]
        query = BidQueryModel(filter,uf,self.storage.cities[uf][city].code,period,values_range)
        result = self.requester.submit_query(query)
        dialog = ResultWindow(result)
        dialog.exec()
        
    
    def initialize_fonts(self):
        self.fontMedium.setPointSize(12)        
        self.fontDefault.setPointSize(10)
