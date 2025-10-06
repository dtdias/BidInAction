from typing import Optional, Mapping, Any


class BidQueryModel:
    filter: str
    uf: str
    city: int
    period: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    page: int
    quantity_per_page: int

    def __init__(
        self,
        filter: str,
        uf: str,
        city: int,
        period: str,
        range_values: Optional[Mapping[str, Any]] = None,
        page: int = 1,
        quantity_per_page: int = 50000,
    ):
        self.filter = filter
        self.uf = uf
        self.city = city
        self.period = period

        # Normaliza e evita KeyError
        self.min_value = None
        self.max_value = None

        if range_values:
            # tenta várias convenções de chave
            raw_max = (
                range_values.get("max", None)
                or range_values.get("max_value", None)
                or range_values.get("valor_maximo", None)
            )
            raw_min = (
                range_values.get("min", None)
                or range_values.get("min_value", None)
                or range_values.get("valor_minimo", None)
            )

            # Converte para float se possível
            def to_float(x):
                if x is None or x == "":
                    return None
                try:
                    # suporta strings com vírgula decimal
                    if isinstance(x, str):
                        x = x.replace(".", "").replace(",", ".") if "," in x else x
                    return float(x)
                except (ValueError, TypeError):
                    return None

            mx = to_float(raw_max)
            mn = to_float(raw_min)

            if mx is not None:
                self.max_value = mx
            if mn is not None:
                self.min_value = mn

        self.page = page
        self.quantity_per_page = quantity_per_page

    def toUrl(self) -> str:
        # Montagem manual conforme seu endpoint espera
        parts = [
            f"codigoDaCidade={self.city}",
            f"dataInicioLance={self.period}",
            f"pagina={self.page}",
            f"quantidadeDeItens={self.quantity_per_page}",
            f"numeroDoLoteOuContrato={self.filter}",
        ]
        if self.max_value is not None:
            parts.append(f"valorMaximoVenda={self.max_value}")
        if self.min_value is not None:
            parts.append(f"valorMinimoVenda={self.min_value}")  # corrigido

        return "&".join(parts)