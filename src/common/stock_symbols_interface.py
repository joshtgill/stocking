from common.database_interface import DatabaseInterface


class StockSymbolsInterface:

    def __init__(self, dataInterface, logInterface):
        self.dataInterface = dataInterface
        self.logInterface = logInterface
        self.databaseInterface = DatabaseInterface(self.dataInterface.settingsGet('stockSymbolsPath'))
        self.upToDate = False


    def saveAll(self, capitalSymbols, globalSymbols, globalSelectSymbols):
        self.save('CAPITAL', capitalSymbols)
        self.save('GLOBAL', globalSymbols)
        self.save('GLOBAL_SELECT', globalSelectSymbols)

        self.upToDate = True


    def save(self, marketType, symbols):
        if not self.databaseInterface.tableExists(marketType):
            self.databaseInterface.createTable(marketType, '(symbol, UNIQUE(symbol))')

        currentSymbols = self.load(marketType)
        for symbol in symbols:
            if symbol not in currentSymbols:
                self.logInterface.log('Adding symbol {} to {}'.format(symbol, marketType))
        for symbol in currentSymbols:
            if symbol not in symbols:
                self.logInterface.log('Removing symbol {} from {}'.format(symbol, marketType))

        sqlFormatSymbols = []
        for symbol in symbols:
            sqlFormatSymbols.append((symbol,))

        self.databaseInterface.insert(marketType, '(symbol)', sqlFormatSymbols)


    def loadAll(self):
        return self.load('CAPITAL') + self.load('GLOBAL') + self.load('GLOBAL_SELECT')


    def load(self, marketType):
        symbols = []
        for item in self.databaseInterface.selectAll(marketType):
            symbols.append(item[0])

        return symbols
