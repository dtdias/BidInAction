from models.bid_model import BidModel
from models.bid_period_model import BidPeriodModel
from models.bid_query_model import BidQueryModel
from models.city_model import CityModel
from models.uf_model import UfModel
import requests


base_url = "https://servicebus2.caixa.gov.br"
api_url = f"{base_url}/vitrinedejoias"
class RequesterService:
    uf_list_url = f"{api_url}/api/busca/ufs/leiloes"
    def request_uf_list(self) -> list[UfModel]:
        results = []
        request = requests.get(self.uf_list_url)
        if request.status_code != 200:
            print("Erro")
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return list(map(lambda o: UfModel(o),results))
    
  
    def request_cities_list(self, uf: str) -> list[CityModel]:
        results = []
        request = requests.get(f"{api_url}/api/busca/cidades/{uf}")
        if request.status_code != 200:
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return list(map(lambda o: CityModel(o) ,results))
    
    def request_bid_period(self, city: int) -> list[BidPeriodModel]:
        results = []
        request = requests.get(f"{api_url}/api/busca/periodos/{city}")
        if request.status_code != 200:
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return list(map(lambda o: BidPeriodModel(o),results))

    def submit_query(self, data: BidQueryModel) -> list[BidModel]:
        results = []
        request = requests.get(f"{api_url}/api/busca/vitrine?{data.toUrl()}")
        if request.status_code != 200:
            return results
        response: dict[str,str | list] = request.json()
        results.extend(response['lotes'])
        return list(map(lambda o: BidModel(o),results))