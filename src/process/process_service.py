from process.statistics.statistics_service import StatisticsService
from process.analyze.minute_analyze_service import MinuteAnalyzeService
from process.analyze.day_analyze_service import DayAnalyzeService
from datetime import datetime, timedelta
import re


class ProcessService():

    def __init__(self, dataInterface, logService, stockDataInterface, tradeService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.tradeService = tradeService
        self.acceptedDayStocks = []


    def go(self):
        self.logService.track('PROCESS')

        serviceDirectory = {'dayAnalyze': self.dayAnalyze, 'minuteAnalyze': self.minuteAnalyze, 'statistics': self.statistics}

        resultSymbols = [] # This is hacky
        for service in self.dataInterface.configGet():
            self.dataInterface.incrementConfig(service)

            if not resultSymbols:
                symbols = self.dataInterface.configGet('symbols')
            else:
                symbols = resultSymbols
            start = self.translateVariable(self.dataInterface.configGet('start'), '1d')
            end = self.translateVariable(self.dataInterface.configGet('end'), '1d')

            resultSymbols = serviceDirectory.get(service)(symbols, start, end)

            self.dataInterface.decrementConfig()

        self.logService.untrack('PROCESS')


    def dayAnalyze(self, symbols, start, end):
        return DayAnalyzeService(self.dataInterface, self.logService, self.stockDataInterface, symbols, start, end).go()


    def minuteAnalyze(self, symbols, start, end):
        MinuteAnalyzeService(self.dataInterface, self.logService, self.stockDataInterface, symbols, start, end).go()


    def statistics(self, symbols, start, end):
        StatisticsService(self.logService, self.stockDataInterface, self.acceptedDayStocks, start, end).go()


    def translateVariable(self, variable, interval):
        if variable == 'NOW':
            return datetime.now().strftime(self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))
        elif 'NOW' in variable:
            marketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')).replace('d', ''))
            return self.determineDate(marketDaysBack).strftime(self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))
        else:
            return variable


    def determineDate(self, marketDaysBack):
        # 2020 stock market holiday closures
        marketClosedDates = [datetime(2020, 1, 1).date(), datetime(2020, 1, 20).date(), datetime(2020, 2, 17).date(),
                             datetime(2020, 4, 10).date(), datetime(2020, 5, 25).date(), datetime(2020, 7, 3).date(),
                             datetime(2020, 9, 7).date(), datetime(2020, 11, 26).date(), datetime(2020, 12, 25).date()]

        # Find the date associated with the number of market days back
        date = datetime.now().date()
        while True:
            if date.weekday() < 5 and date not in marketClosedDates:
                marketDaysBack -= 1

            if not marketDaysBack:
                break

            date = date - timedelta(days=1)

        return date
