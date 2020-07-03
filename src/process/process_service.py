from datetime import datetime, timedelta
import re
from process.analyze.analyze_service import AnalyzeService


class ProcessService():

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService


    def go(self):
        for interval in self.configInterface.get():
            symbols = self.configInterface.get('{}/symbols'.format(interval))
            start = self.translateVariable(self.configInterface.get('{}/start'.format(interval)))
            end = self.translateVariable(self.configInterface.get('{}/end'.format(interval)))
            for module in self.configInterface.get('{}/modules'.format(interval)):
                self.logService.register(module)
                self.logService.log(module, 'Analyzing {}'.format(interval), 'info')
                AnalyzeService(interval, symbols, start, end).go()
                self.logService.unregister(module)


    def translateVariable(self, variable):
        if variable == 'NOW':
            return datetime.now().strftime('%Y-%m-%d')
        elif 'NOW' in variable:
            marketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')))
            return self.determineDate(marketDaysBack).strftime('%Y-%m-%d')
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
