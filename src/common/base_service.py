from datetime import datetime, timedelta
import re


class BaseService:

    def __init__(self, name, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface):
        self.name = name
        self.dataInterface = dataInterface
        self.logInterface = logInterface
        self.stockSymbolsInterface = stockSymbolsInterface
        self.stockHistoryInterface = stockHistoryInterface


    def start(self, *args):
        self.logInterface.start(self.name)

        self.go(*args)

        self.logInterface.stop(self.name)


    def translateConfigVariable(self, variable):
        if variable == 'CAPITAL':
            return self.stockSymbolsInterface.load('CAPITAL')
        elif variable == 'GLOBAL':
            return self.stockSymbolsInterface.load('GLOBAL')
        elif variable == 'GLOBAL_SELECT':
            return self.stockSymbolsInterface.load('GLOBAL_SELECT')
        elif variable == 'ALL':
            return self.stockSymbolsInterface.loadAll()
        elif variable == 'NOW':
            return datetime.now().strftime(self.dataInterface.settingsGet('{}/dateTimeFormat'.format('day')))
        elif 'NOW' in variable:
            openMarketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')).replace('d', ''))
            return self.determineDate(openMarketDaysBack).strftime(self.dataInterface.settingsGet('{}/dateTimeFormat'.format('day')))

        return variable


    def determineDate(self, openMarketDaysBack):
        # 2021 market holiday closures
        marketClosedDates = [datetime(2021, 1, 1).date(), datetime(2021, 1, 18).date(), datetime(2021, 2, 15).date(),
                             datetime(2021, 4, 2).date(), datetime(2021, 5, 31).date(), datetime(2021, 7, 5).date(),
                             datetime(2021, 9, 6).date(), datetime(2021, 11, 25).date(), datetime(2021, 12, 24).date()]

        # Find the date associated with the number of market days back
        date = datetime.now().date()
        while True:
            if date.weekday() < 5 and date not in marketClosedDates:
                openMarketDaysBack -= 1

            if not openMarketDaysBack:
                break

            date = date - timedelta(days=1)

        return date
