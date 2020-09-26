from common.base_service import BaseService
from process.analyze.minute_analyze_service import MinuteAnalyzeService
from process.analyze.day_analyze_service import DayAnalyzeService
from datetime import datetime, timedelta
import re


class ProcessService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface, dayAnalyzeService, minuteAnalyzeService):
        super().__init__('PROCESS', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)
        self.dayAnalyzeService = dayAnalyzeService
        self.minuteAnalyzeService = minuteAnalyzeService


    def go(self):
        moduleDirectory = {'dayAnalyze': self.dayAnalyze, 'minuteAnalyze': self.minuteAnalyze}

        module = self.dataInterface.configGet('module')
        symbols = self.dataInterface.configGet('symbols')
        start = self.translateConfigVariable(self.dataInterface.configGet('start'))
        end = self.translateConfigVariable(self.dataInterface.configGet('end'))

        moduleDirectory.get(module)(symbols, start, end)


    def dayAnalyze(self, symbols, start, end):
        return self.dayAnalyzeService.go(symbols, start, end)


    def minuteAnalyze(self, symbols, start, end):
        return self.minuteAnalyzeService.go(symbols, start, end)
