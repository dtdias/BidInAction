from models.bid_period_model import BidPeriodModel
from models.city_model import CityModel
from models.uf_model import UfModel


class StorageService:
    cities: dict[str, dict[str,CityModel]] = {}
    periods: dict[str, dict[str,BidPeriodModel]] = {}
    values_range = {
        "Todos": {"min": 0},
        "Abaixo de R$ 500,00": {"min": 0, "max": 500},
        "De R$ 500,01 à R$ 1.000,00": {"min": 500.01, "max": 1000},
        "De R$ 1.000,01 à R$ 1.500,00": {"min": 1000.01, "max": 1500},
        "De R$ 1500,01 à R$ 2.000,00": {"min": 1500.01, "max": 2000},
        "De R$ 2000,01 à R$ 3.000,00": {"min": 2000.01, "max": 3000},
        "Acima de R$ 3.000,00": {"min": 3000.01},
    }
    
    def __init__(self):
        pass