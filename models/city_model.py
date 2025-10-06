class CityModel:
    code: int
    name: str
    uf: str
    def __init__(self, data):
        self.code = data['codigo']
        self.name = data['nome']
        self.uf = data['siglaUf']
