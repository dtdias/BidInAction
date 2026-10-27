from dataclasses import dataclass

from models.bid_model import PublishedFile


@dataclass(frozen=True)
class AuctionModel:
    code: str
    uf: str
    city: str
    centralizing_unit: str
    status: str
    bid_period: str
    exposure_period: str
    pickup_period: str
    documents: list[PublishedFile]

    @classmethod
    def from_api(cls, data: dict) -> "AuctionModel":
        def date_range(start: str, end: str) -> str:
            if not start or not end:
                return ""
            return f"{start[:10]} a {end[:10]}"

        return cls(
            code=str(data.get("leilao", "")),
            uf=str(data.get("uf", "")),
            city=str(data.get("municipio", "")),
            centralizing_unit=str(data.get("unidadeCentralizadora", "")),
            status=str(data.get("situacao", "")),
            bid_period=date_range(data.get("dataDeLanceInicio", ""), data.get("dataDeLanceFim", "")),
            exposure_period=date_range(
                data.get("periodoDeExposicaoInicio", ""), data.get("periodoDeExposicaoFim", "")
            ),
            pickup_period=date_range(
                data.get("periodoDeRetiradaInicio", ""), data.get("periodoDeRetiradaFim", "")
            ),
            documents=[PublishedFile.from_api(item) for item in data.get("arquivosPublicados", [])],
        )

    @property
    def label(self) -> str:
        return f"{self.code} | {self.city} | {self.status}"
