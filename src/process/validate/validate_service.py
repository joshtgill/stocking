from common.base_service import BaseService
from datetime import datetime, timedelta


class ValidateService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface):
        super().__init__('VALIDATE', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)
        self.marketCloseExceptions = [datetime(2018, 12, 5), datetime(2012, 10, 29), datetime(2004, 6, 11), datetime(2001, 9, 11)]
        # Directory where the key represents a month, and the value represents the number of
        # holidays, or days without stock history, during that month
        self.monthHolidayCountDirectory = {1: 2, 2: 1, 3: 0.5, 4: 0.5, 5: 1, 7: 1, 9: 1, 11: 1, 12: 1}


    def go(self):
        interval = self.dataInterface.configGet('interval')
        symbols = self.translateConfigVariable(self.dataInterface.configGet('symbols'))
        minimumYear = self.dataInterface.configGet('minimumYear')

        for symbol in symbols:
            self.validateStockHistory(symbol, interval, minimumYear)


    def validateStockHistory(self, symbol, interval, minimumYear):
        self.stockHistoryInterface.load(interval, symbol)

        activeDateTime = datetime.strptime(self.stockHistoryInterface.next()[0],
                                           self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d' else
                                           self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        monthHolidayCountDirectory = dict(self.monthHolidayCountDirectory)
        activeYear = activeDateTime.year
        while self.stockHistoryInterface.next():
            # On a year change, reset month-holiday directory
            if activeDateTime.year != activeYear:
                activeYear = activeDateTime.year
                monthHolidayCountDirectory = dict(self.monthHolidayCountDirectory)

            # Not including holidays, determine the next expected date/time
            nextExpectedDateTime = self.getNextExpectedDateTime(interval, activeDateTime)

            # Observed next date/time
            nextDateTime = datetime.strptime(self.stockHistoryInterface.peek()[0],
                                             self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d' else
                                             self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

            # If there is a discrepancy that is after minimumYear, attribute it to a holiday.
            # If no remaining holidays, report an error
            if nextDateTime != nextExpectedDateTime:
                if nextExpectedDateTime.year < minimumYear or nextExpectedDateTime in self.marketCloseExceptions:
                    continue

                holidayCount = monthHolidayCountDirectory.get(nextExpectedDateTime.month)

                if holidayCount and holidayCount > 0:
                    monthHolidayCountDirectory.update({nextExpectedDateTime.month: holidayCount - 1})
                else:
                    self.logInterface.log('Missing history for {} ({}) on {}'.format(symbol, interval, nextExpectedDateTime), 'WARN')

            activeDateTime = nextDateTime


    def getNextExpectedDateTime(self, interval, activeDateTime):
        nextDateTime = None

        if interval == '1d':
            nextDateTime = activeDateTime + timedelta(days=1)

            # Correct weekend
            if nextDateTime.weekday() == 5:
                nextDateTime = nextDateTime + timedelta(days=2)
            elif nextDateTime.weekday() == 6:
                nextDateTime = nextDateTime + timedelta(days=1)


        return nextDateTime
