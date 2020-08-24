import json
import yfinance


class DisplayService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self):
        self.logService.start('DISPLAY')

        number = self.dataInterface.configGet('number')

        symbols = []
        with open('exe/symbols/good_symbols_{}.json'.format(number)) as filee:
            symbols = json.load(filee)

        for symbol in symbols:
            self.displayStockInfo(symbol)
            # self.displayStockData(symbol, interval)
            # print()

        self.logService.stop('DISPLAY')


    def displayStockData(self, symbol, interval):
        self.stockDataInterface.load(interval, symbol)

        while self.stockDataInterface.next():
            print(self.stockDataInterface.peek())


    def displayStockInfo(self, symbol):
        try:
            volume = yfinance.Ticker(symbol).info.get('volume')
            print(symbol)
        except:
            print('failed')
