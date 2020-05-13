from datetime import datetime
import yfinance
import pandas
import pytz


class TradeService():

    def __init__(self, stockDataInterface):
        self.stockDataInterface = stockDataInterface
        self.buyTrades, self.sellTrades = self.buildTradeData()
        self.stocksTrading = self.loadStocksTrading()
        self.timeFrame = self.loadTimeFrame()


    def buildTradeData(self):
        buys = {}
        for buy in self.tradeConfig.get('buys'):
            buys.update({datetime.strptime(buy.get('datetime'), '%Y-%m-%d %H:%M:%S'): (buy.get('symbol'), buy.get('shares'))})

        sells = {}
        for sell in self.tradeConfig.get('sells'):
            sells.update({datetime.strptime(sell.get('datetime'), '%Y-%m-%d %H:%M:%S'): (sell.get('symbol'), sell.get('shares'))})

        return buys, sells


    def loadStocksTrading(self):
        stocks = {}
        for dateTimeKey in self.buyTrades:
            stock = self.stockDataInterface.load(self.buyTrades.get(dateTimeKey)[0], '1m')
            stocks.update({stock.symbol: stock.history})

        return stocks


    def loadTimeFrame(self):
        timeFrame = []
        for historyItem in self.stocksTrading.get(list(self.stocksTrading.keys())[0]):
            timeFrame.append(datetime.strptime(historyItem[0], '%Y-%m-%d %H:%M:%S'))

        return timeFrame


    def simulateTrading(self):
        for i in range(len(self.timeFrame)):
            dateTime = self.timeFrame[i]
            if self.buyTrades.get(dateTime):
                buySymbol = self.buyTrades.get(dateTime)[0]
                buyPrice = self.stocksTrading.get(buySymbol)[i][1]
                print('Bought {} at {} per share.'.format(buySymbol, buyPrice))
            if self.sellTrades.get(dateTime):
                sellSymbol = self.sellTrades.get(dateTime)[0]
                sellPrice = self.stocksTrading.get(sellSymbol)[i][1]
                print('Sold {} at {} per share.'.format(sellSymbol, sellPrice))
