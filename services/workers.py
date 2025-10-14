from PySide6.QtCore import QObject, Signal, Slot
from services.request_service import RequesterService
from models.bid_query_model import BidQueryModel

class SearchWorker(QObject):
    finished = Signal(list)   # será emitido com a lista de resultados
    failed = Signal(str)      # será emitido com a mensagem de erro

    def __init__(self, query: BidQueryModel):
        super().__init__()
        self.query = query
        self.requester = RequesterService()

    @Slot()
    def run(self):
        try:
            results = self.requester.submit_query(self.query)
            self.finished.emit(results)
        except Exception as e:
            self.failed.emit(str(e))