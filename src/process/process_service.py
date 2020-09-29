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
        self.moduleDirectory = {'day_analyze': self.dayAnalyzeService, 'minute_analyze': self.minuteAnalyzeService}


    def go(self, *args):
        symbols = self.translateConfigVariable(self.dataInterface.configGet('symbols'))
        modulesData = self.translateConfigVariable(self.dataInterface.configGet('modules'))

        for i in range(len(modulesData)):
            self.dataInterface.incrementConfig('modules/[{}]'.format(i))

            self.moduleDirectory.get(modulesData[i].get('name')).start(symbols)

            self.dataInterface.decrementConfig()
