from common.base_service import BaseService
from statistics import mean, stdev
import yfinance as yf
import threading


class MinuteAnalyzeService(BaseService):

    def __init__(self, dataInterface, logService, stockHistoryInterface, dayAnalyzeService):
        super().__init__('MINUTE ANALYZE', dataInterface, logService)
        self.stockHistoryInterface = stockHistoryInterface
        self.dayAnalyzeService = dayAnalyzeService


    def go(self, symbols, start, end):
        pass
