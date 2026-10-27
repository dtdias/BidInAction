import base64
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PublishedFile:
    identifier: str
    transaction: str
    name: str
    file_type: str

    @classmethod
    def from_api(cls, data: dict) -> "PublishedFile":
        return cls(
            identifier=str(data.get("CodIdentificacao", "")),
            transaction=str(data.get("CodTransacao", "")),
            name=str(data.get("Nome", "")),
            file_type=str(data.get("NomeTipoArquivo", "Documento")),
        )


@dataclass(frozen=True)
class BidPhoto:
    name: str
    encoded: str

    @classmethod
    def from_api(cls, data: dict) -> "BidPhoto":
        return cls(str(data.get("nomeArquivo", "")), str(data.get("base64", "")))

    def bytes(self) -> bytes:
        encoded = self.encoded.split(",", 1)[-1]
        return base64.b64decode(encoded, validate=True)


@dataclass
class BidModel:
    contract_number: str
    batch_number: str
    value: str
    bid_code: str
    uf_acronym: str = ""
    centralizing_name: str = ""
    bid_date: str = ""
    result_date: str = ""
    contract_description: str = ""
    local_address_description: str = ""
    photos: list[BidPhoto] = field(default_factory=list)
    published_files: list[PublishedFile] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict, auction: dict | None = None) -> "BidModel":
        auction = auction or {}
        return cls(
            contract_number=str(data.get("numeroContrato", "")),
            batch_number=str(data.get("lote", data.get("numeroLote", ""))),
            value=str(data.get("valor", "")),
            bid_code=str(data.get("leilao", auction.get("leilao", ""))),
            uf_acronym=str(auction.get("siglaUf", auction.get("uf", ""))),
            centralizing_name=str(
                auction.get("agenciaCentralizadora", auction.get("unidadeCentralizadora", ""))
            ),
            bid_date=str(auction.get("periodoDeLance", "")),
            photos=[BidPhoto.from_api(photo) for photo in data.get("fotos", [])],
            published_files=[
                PublishedFile.from_api(item)
                for item in auction.get("arquivosPublicados", [])
            ],
        )


@dataclass(frozen=True)
class BidSearchResult:
    lots: list[BidModel]
    total: int
    auction: dict
    message: str = ""


@dataclass(frozen=True)
class BidDetail:
    description: str
    value: str
    lot_number: str
    contract_number: str
    result_date: str
    pickup_address: str

    @classmethod
    def from_api(cls, data: dict) -> "BidDetail":
        return cls(
            description=str(data.get("descricao", "")),
            value=str(data.get("valor", "")),
            lot_number=str(data.get("numeroLote", "")),
            contract_number=str(data.get("numeroContrato", "")),
            result_date=str(data.get("dataResultadoApuracao", "")),
            pickup_address=str(data.get("enderecoRetirada", "")),
        )
