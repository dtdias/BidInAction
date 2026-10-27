import unittest

from models.bid_model import PublishedFile
from models.bid_query_model import BidQueryModel
from services.request_service import API_URL, RequesterService


class FakeResponse:
    def __init__(self, payload=None, content=b"", headers=None):
        self.payload = payload
        self.content = content
        self.headers = headers or {}

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.get_calls = []
        self.post_calls = []
        self.responses = []

    def get(self, url, timeout, **kwargs):
        self.get_calls.append((url, timeout, kwargs))
        return self.responses.pop(0)

    def post(self, url, data, timeout):
        self.post_calls.append((url, data, timeout))
        return self.responses.pop(0)


class RequesterServiceTests(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.service = RequesterService(self.session)

    def test_schedule_uses_zero_padded_month(self):
        schedule = {"leiloes": []}
        self.session.responses.append(FakeResponse(schedule))

        self.assertEqual(self.service.request_schedule(2026, 3), schedule)
        self.assertEqual(self.session.get_calls[0][0], f"{API_URL}/api/cronograma/2026/03")
        self.assertEqual(self.session.get_calls[0][1], 10)

    def test_lot_query_uses_observed_parameters_and_maps_response(self):
        self.session.responses.append(
            FakeResponse(
                {
                    "contratos": [
                        {
                            "numeroContrato": "0281.213.00024062-5",
                            "lote": "0281.000003-9",
                            "valor": "R$3.430,00",
                            "leilao": "336/2026",
                            "fotos": [],
                        }
                    ],
                    "totalRegistros": 204,
                    "cronogramaLeilao": {
                        "siglaUf": "SP",
                        "agenciaCentralizadora": "281 - ARACATUBA, SP",
                    },
                }
            )
        )
        query = BidQueryModel(
            auction_code="336/2026",
            page=2,
            limit=24,
            sort="valorMinimoVenda",
            descending=True,
            min_value=500.01,
            max_value=1000,
            description="anel",
        )

        result = self.service.request_lots(query)

        url, _, kwargs = self.session.get_calls[0]
        self.assertEqual(url, f"{API_URL}/api/cronograma/contratos")
        self.assertEqual(
            kwargs["params"],
            {
                "coleilao": "336/2026",
                "pagina": 2,
                "limit": 24,
                "desc": True,
                "sort": "valorMinimoVenda",
                "valorInicial": 500.01,
                "valorFinal": 1000,
                "descricaoLote": "anel",
            },
        )
        self.assertEqual(result.total, 204)
        self.assertEqual(result.lots[0].uf_acronym, "SP")

    def test_lot_number_uses_dedicated_search_parameter(self):
        query = BidQueryModel(auction_code="336/2026", lot_number="0281000003-9")

        self.assertEqual(
            query.to_params(),
            {"coleilao": "336/2026", "pagina": 1, "limit": 12, "nuLote": "0281000003-9"},
        )

    def test_detail_and_document_download(self):
        self.session.responses.extend(
            [
                FakeResponse(
                    {
                        "descricao": "ANEL",
                        "valor": "R$1,00",
                        "numeroLote": "1",
                        "numeroContrato": "2",
                        "dataResultadoApuracao": "03/11/2026",
                        "enderecoRetirada": "ENDERECO",
                    }
                ),
                FakeResponse(
                    content=b"%PDF-1.6",
                    headers={
                        "content-type": "application/pdf",
                        "content-disposition": "attachment; filename=Edital.pdf",
                    },
                ),
            ]
        )

        detail = self.service.request_lot_detail("336/2026", "2")
        download = self.service.download_documents([PublishedFile("id", "tx", "Edital", "Edital")])

        self.assertEqual(detail.pickup_address, "ENDERECO")
        self.assertEqual(
            self.session.get_calls[0][2]["params"],
            {"codigoLeilao": "336/2026", "numeroContrato": "2"},
        )
        self.assertEqual(self.session.post_calls[0][1], [("documentos[]", "id"), ("transacao", "tx")])
        self.assertEqual(download.filename, "Edital.pdf")
        self.assertEqual(download.content, b"%PDF-1.6")

    def test_content_endpoints_use_expected_paths(self):
        self.session.responses.extend([FakeResponse({}) for _ in range(4)])

        self.service.request_header()
        self.service.request_footer()
        self.service.request_related_links()
        self.service.request_service_channels()

        self.assertEqual(
            [call[0] for call in self.session.get_calls],
            [
                f"{API_URL}/api/cabecalho",
                f"{API_URL}/api/Rodape",
                f"{API_URL}/api/VejaTambem",
                f"{API_URL}/api/CanaisDeAtendimento",
            ],
        )


if __name__ == "__main__":
    unittest.main()
