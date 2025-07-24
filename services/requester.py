from h11 import Request
import requests


base_url = "https://servicebus2.caixa.gov.br"
api_url = f"{base_url}/vitrinedejoias"
photos_url = f"{base_url}/vitrinearquivos/fotos"
class Requester:
    uf_list_url = f"{api_url}/api/busca/ufs/leiloes"
    def request_uf_list(self) -> list[str]:
        results = []
        request = requests.get(self.uf_list_url)
        if request.status_code != 200:
            print("Erro")
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return list(map(self.__perform_request_uf_list,results))
    
  
    def request_cities_list(self, uf: str) -> list[dict]:
        results = []
        request = requests.get(f"{api_url}/api/busca/cidades/{uf}")
        if request.status_code != 200:
            print("Erro")
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return results
    
    def request_bid_period(self, city: int) -> list[dict]:
        results = []
        request = requests.get(f"{api_url}/api/busca/periodos/{city}")
        if request.status_code != 200:
            print("Erro")
            return results
        
        response: list[dict[str,str]] = request.json()
        list.extend(results, response)
        return results

    def __perform_request_uf_list(self,o: dict[str, str]):
            return o['sigla']
    