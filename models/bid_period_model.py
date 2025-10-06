class BidPeriodModel:
    start_date: str
    end_date: str
    bid_period: str
    def __init__(self, data):
        self.start_date = data['inicioLance']
        self.end_date = data['fimLance']
        self.bid_period = data['periodoDeLance']