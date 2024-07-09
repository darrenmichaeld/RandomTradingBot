# region imports
from AlgorithmImports import *
# endregion

class FirstBotCreated(QCAlgorithm):

    def initialize(self):
        # Set Start and End Date
        self.set_start_date(2020, 5, 8)
        self.set_end_date(2020, 6, 8)

        # Set Initial Cash & Company to be traded (with daily resolution)
        self.set_cash(100000)
        spy = self.add_equity("SPY", Resolution.DAILY)
        spy.set_data_normalization_mode(DataNormalizationMode.Raw)

        # Use symbol as it has better information included than tick data
        self.spy = spy.symbol

        self.set_benchmark("SPY")

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.time

    def on_data(self, data: Slice):
        if not self.spy in data:
            return

        price = data[self.spy].close

        if not self.portfolio.invested:
            self.set_holdings("SPY", 1)
            self.log("Buy SPY @" + str(price))
            self.entryPrice = price

        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.liquidate()
            self.log("Sell SPY @" + str(price))
            self.nextEntryTime = self.time + self.period
