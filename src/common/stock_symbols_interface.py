import urllib.request
from common.database_interface import DatabaseInterface
import sqlite3


class StockSymbolsInterface:

    def __init__(self, dataInterface, logService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.databaseInterface = DatabaseInterface(self.dataInterface.settingsGet('stockSymbolsPath'))


    def saveAll(self, capitalSymbols, globalSymbols, globalSelectSymbols):
        self.save('CAPITAL', capitalSymbols)
        self.save('GLOBAL', globalSymbols)
        self.save('GLOBAL_SELECT', globalSelectSymbols)


    def save(self, marketType, symbols):
        currentSymbols = self.load(marketType)
        for symbol in symbols:
            if symbol not in currentSymbols:
                self.logService.log('Adding symbol {} to {}'.format(symbol, marketType))
        for symbol in currentSymbols:
            if symbol not in symbols:
                self.logService.log('Removing symbol {} from {}'.format(marketType))

        sqlFormatSymbols = []
        for symbol in symbols:
            sqlFormatSymbols.append((symbol,))

        self.databaseInterface.insertSymbols(marketType, sqlFormatSymbols)


    def load(self, marketType):
        symbols = []
        for item in self.databaseInterface.selectAll(marketType):
            symbols.append(item[0])

        return symbols
