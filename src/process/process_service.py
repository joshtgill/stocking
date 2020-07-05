from datetime import datetime, timedelta
import re
from process.analyze.day_analyze_service import DayAnalyzeService


class ProcessService():

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService
        self.logService.register('PROCESS')


    def __del__(self):
        self.logService.unregister('PROCESS')


    def go(self):
        for interval in self.configInterface.configGet():
            symbols = self.configInterface.configGet('{}/symbols'.format(interval))
            start = self.translateVariable(self.configInterface.configGet('{}/start'.format(interval)), interval)
            end = self.translateVariable(self.configInterface.configGet('{}/end'.format(interval)), interval)
            for module in self.configInterface.configGet('{}/modules'.format(interval)):
                DayAnalyzeService(symbols, start, end).go()


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
