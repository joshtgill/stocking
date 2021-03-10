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
        for moduleName, moduleData in self.dataInterface.configGet('modules').items():
            self.dataInterface.incrementConfig('modules/{}'.format(moduleName))

            self.moduleDirectory.get(moduleName).start()

            self.dataInterface.decrementConfig()
