from datetime import date


class PublishedFiles:
    name: str
    type: str
    def __init__(self, data):
        self.name = data['nome']
        self.type = data['tipoArquivo']

class BidModel:
    id: str
    published_files: list[PublishedFiles]
    bid_code: str
    bid_date: date
    publish_date: date 
    result_date: date
    start_date: date
    end_date: date
    contract_description: str
    centralizing_name: str
    local_adress_description: str
    public_notice: str
    catalog: str
    unity_number: int
    contract_number: str
    batch_number: str
    natural_number: int
    uf_acronym: str
    value: str
    url_image_cover: str
    url_image_front: str
    url_image_front_small: str
    url_image_back: str
    url_image_back_small: str
    
    def __init__(self, data):
        print(data)
        self.id = data['id']
        self.published_files = list([PublishedFiles(x) for x in data['arquivosPublicados']])
        self.bid_code = data['coLeilao']
        self.bid_date = data['dataDeLance']
        self.publish_date = data['dataDivulgacao']
        self.result_date = data['dataResultado']
        self.start_date = data['dataInicio']
        self.end_date = data['dataFim']
        self.contract_description = data['deContrato']
        self.centralizing_name = data['noCentralizadora']
        self.local_adress_description = data['deLocalEndereco']
        self.public_notice = data['edital']
        self.catalog = data['catalogo']
        self.unity_number = data['nuUnidade']
        self.contract_number = data['nuContrato']
        self.batch_number = data['numeroDolote']
        self.natural_number = data['nuNatural']
        self.uf_acronym = data['sgUf']
        self.value = data['valor']
        self.url_image_cover = data['urlImagemCapa']
        self.url_image_front = data['urlImagemFrente']
        self.url_image_front_small = data['urlImagemFrenteP']
        self.url_image_back = data['urlImagemVerso']
        self.url_image_back_small = data['urlImagemVersoP']