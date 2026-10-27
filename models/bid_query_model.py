from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BidQueryModel:
    auction_code: str
    page: int = 1
    limit: int = 12
    sort: str = "nuLote"
    descending: bool = False
    min_value: float = 0
    max_value: float = 0
    description: str = ""
    lot_number: str = ""

    def to_params(self) -> dict[str, str | int | float | bool]:
        params: dict[str, str | int | float | bool] = {
            "coleilao": self.auction_code,
            "pagina": self.page,
            "limit": self.limit,
        }
        if self.lot_number:
            params["nuLote"] = self.lot_number
            return params

        params.update(
            {
                "desc": self.descending,
                "sort": self.sort,
                "valorInicial": self.min_value,
                "valorFinal": self.max_value,
            }
        )
        if self.description:
            params["descricaoLote"] = self.description
        return params
