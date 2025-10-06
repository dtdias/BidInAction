from typing import Optional
from urllib.parse import urlencode


class BidQueryModel:
    filter: str
    uf: str
    city: int
    period: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    page: int
    quantity_per_page: int
    def __init__(self, 
                 filter: str, uf: str, city: int, period: str, range_values: dict[str, float], 
                 page = 1, quantity_per_page = 10000 
                 ):
        self.filter = filter
        self.uf = uf
        self.city = city
        self.period = period
        if range_values["max"]:
            self.max_value = range_values["max"]
        if range_values["min"]:
            self.min_value = range_values["min"]
        self.page = page
        self.quantity_per_page = quantity_per_page

    def toUrl(self):
        result = f"codigoDaCidade={self.city}&dataInicioLance={self.period}&pagina={self.page}&quantidadeDeItens={self.quantity_per_page}&numeroDoLoteOuContrato={self.filter}"
        if self.max_value != None:
            result += f"&valorMaximoVenda={self.max_value}"
            
        if self.min_value != None:
            result += f"&valorMaximoVenda={self.min_value}"

        return result