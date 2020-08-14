from process.analyze.minute_analyze_service import MinuteAnalyzeService
from process.analyze.day_analyze_service import DayAnalyzeService
from datetime import datetime, timedelta
import re


class ProcessService():

    def __init__(self, dataInterface, logService, stockDataInterface, dayAnalyzeService, minuteAnalyzeService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.dayAnalyzeService = dayAnalyzeService
        self.minuteAnalyzeService = minuteAnalyzeService
        self.passedSymbols = []


    def go(self):
        self.logService.track('PROCESS')

        serviceDirectory = {'1d': self.dayAnalyze, '1m': self.minuteAnalyze}

        interval = self.dataInterface.configGet('interval')
        symbols = self.dataInterface.configGet('symbols')
        start = self.dataInterface.configGet('start')
        end = self.dataInterface.configGet('end')

        self.passedSymbols = serviceDirectory.get(interval)(symbols, start, end)

        self.logService.untrack('PROCESS')


    def dayAnalyze(self, symbols, start, end):
        return self.dayAnalyzeService.go(symbols, start, end)


    def minuteAnalyze(self, symbols, start, end):
        return self.minuteAnalyzeService.go(symbols, start, end)
