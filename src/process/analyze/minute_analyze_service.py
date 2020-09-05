from statistics import mean, stdev
import yfinance as yf
import threading


class MinuteAnalyzeService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self, symbols, start, end):
        self.logService.start('MINUTE ANALYZE')

        self.logService.stop('MINUTE ANALYZE')
