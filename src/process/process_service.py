from process.analyze.macro_analyze_service import MacroAnalyzeService
from process.analyze.micro_analyze_service import MicroAnalyzeService
from datetime import datetime, timedelta
import re


class ProcessService():

    def __init__(self, configInterface, logService, tradeService):
        self.configInterface = configInterface
        self.logService = logService
        self.tradeService = tradeService


    def __del__(self):
        self.logService.untrack('PROCESS')


    def go(self):
        self.logService.track('PROCESS')

        for processConfigItem in self.configInterface.configGet():
            interval = processConfigItem.get('interval')
            symbols = processConfigItem.get('symbols')
            start = self.translateVariable(processConfigItem.get('start'), interval)
            end = self.translateVariable(processConfigItem.get('end'), interval)
            for module in processConfigItem.get('modules'):
                if interval == '1d':
                    MacroAnalyzeService(self.configInterface, self.logService, symbols, start, end).go()
                elif interval == '1m':
                    MicroAnalyzeService(self.configInterface, self.logService, symbols, start, end).go()


    def translateVariable(self, variable, interval):
        if variable == 'NOW':
            return datetime.now().strftime(self.configInterface.settingsGet('{}/dateTimeFormat'.format(interval)))
        elif 'NOW' in variable:
            marketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')).replace('d', ''))
            return self.determineDate(marketDaysBack).strftime(self.configInterface.settingsGet('{}/dateTimeFormat'.format(interval)))
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
