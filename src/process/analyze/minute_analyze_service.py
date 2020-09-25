from statistics import mean, stdev
import yfinance as yf
import threading


class MinuteAnalyzeService:

    def __init__(self, dataInterface, logService, stockHistoryInterface, dayAnalyzeService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockHistoryInterface = stockHistoryInterface
        self.dayAnalyzeService = dayAnalyzeService


    def go(self, symbols, start, end):
        self.logService.start('MINUTE ANALYZE')

        self.logService.stop('MINUTE ANALYZE')
