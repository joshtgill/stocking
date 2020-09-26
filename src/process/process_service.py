from common.base_service import BaseService
from process.analyze.day_analyze_service import DayAnalyzeService
from process.analyze.minute_analyze_service import MinuteAnalyzeService
from datetime import datetime, timedelta
import re


class ProcessService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface, dayAnalyzeService, minuteAnalyzeService):
        super().__init__('PROCESS', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)
        self.dayAnalyzeService = dayAnalyzeService
        self.minuteAnalyzeService = minuteAnalyzeService


    def go(self):
        symbols = self.translateConfigVariable(self.dataInterface.configGet('symbols'))
        start = self.translateConfigVariable(self.dataInterface.configGet('start'))
        end = self.translateConfigVariable(self.dataInterface.configGet('end'))

        self.dayAnalyzeService.go(symbols, start, end)
        self.minuteAnalyzeService.go(symbols, start, end)
