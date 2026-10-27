from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from models.bid_model import BidDetail, BidModel, BidSearchResult, PublishedFile
from models.bid_query_model import BidQueryModel


API_URL = "https://servicebus2.caixa.gov.br/portalvitrinedejoias"


@dataclass(frozen=True)
class DownloadedFile:
    filename: str
    content: bytes
    content_type: str


class RequesterService:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()

    def _get(self, path: str, timeout: int = 30, **kwargs) -> Any:
        response = self.session.get(f"{API_URL}{path}", timeout=timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    def request_schedule(self, year: int, month: int) -> dict:
        return self._get(f"/api/cronograma/{year}/{month:02d}", timeout=10)

    def request_lots(self, query: BidQueryModel) -> BidSearchResult:
        payload = self._get("/api/cronograma/contratos", params=query.to_params())
        auction = payload.get("cronogramaLeilao", {})
        return BidSearchResult(
            lots=[BidModel.from_api(item, auction) for item in payload.get("contratos", [])],
            total=int(payload.get("totalRegistros", 0)),
            auction=auction,
            message=str((payload.get("mensagemRetorno") or {}).get("texto", "")),
        )

    def request_lot_detail(self, auction_code: str, contract_number: str) -> BidDetail:
        payload = self._get(
            "/api/cronograma/contrato",
            params={"codigoLeilao": auction_code, "numeroContrato": contract_number},
        )
        return BidDetail.from_api(payload)

    def download_documents(self, documents: list[PublishedFile]) -> DownloadedFile:
        if not documents:
            raise ValueError("Nenhum documento selecionado.")
        transactions = {item.transaction for item in documents}
        if len(transactions) != 1 or not next(iter(transactions)):
            raise ValueError("Documentos devem pertencer ao mesmo leilão.")
        response = self.session.post(
            f"{API_URL}/api/cronograma/downloads",
            data=[("documentos[]", item.identifier) for item in documents]
            + [("transacao", next(iter(transactions)))],
            timeout=60,
        )
        response.raise_for_status()
        disposition = response.headers.get("content-disposition", "")
        filename = "Documentos.zip" if len(documents) > 1 else f"{documents[0].name}.pdf"
        if "filename=" in disposition:
            filename = disposition.split("filename=", 1)[1].strip(' \"')
        return DownloadedFile(filename, response.content, response.headers.get("content-type", ""))

    def save_download(self, download: DownloadedFile, destination: str) -> None:
        Path(destination).write_bytes(download.content)

    def request_header(self) -> Any:
        return self._get("/api/cabecalho")

    def request_footer(self) -> Any:
        return self._get("/api/Rodape")

    def request_related_links(self) -> Any:
        return self._get("/api/VejaTambem")

    def request_service_channels(self) -> Any:
        return self._get("/api/CanaisDeAtendimento")
