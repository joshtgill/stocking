from datetime import datetime
import yfinance
import pandas
import pytz


class TradeService():

    def __init__(self, tradeConfig, stockDataInterface):
        self.tradeConfig = tradeConfig
        self.stockDataInterface = stockDataInterface
        self.buyTrades, self.sellTrades = self.buildTradeData()
        self.stocks = self.loadRelevantStocks()


    def buildTradeData(self):
        buys = {}
        for buy in self.tradeConfig.get('buys'):
            buys.update({datetime.strptime(buy.get('datetime'), '%Y-%m-%d %H:%M:%S'): (buy.get('symbol'), buy.get('shares'))})

        sells = {}
        for sell in self.tradeConfig.get('sells'):
            sells.update({datetime.strptime(sell.get('datetime'), '%Y-%m-%d %H:%M:%S'): (sell.get('symbol'), sell.get('shares'))})

        return buys, sells


    def loadRelevantStocks(self):
        stocks = {}
        for dateTimeKey in self.buyTrades:
            stock = self.stockDataInterface.load(self.buyTrades.get(dateTimeKey)[0], '1d')
            stocks.update({stock.symbol: stock.history})

        return stocks


    def simulateTrading(self):
        return