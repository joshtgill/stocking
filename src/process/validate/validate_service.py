from datetime import datetime, timedelta


class ValidateService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        # Directory where the key represents a month, and the value represents the number of
        # holidays, or days without stock data, during that month
        self.monthHolidayCountDirectory = {1: 2, 2: 1, 3: 0.5, 4: 0.5, 5: 1, 7: 1, 9: 1, 11: 1, 12: 1}


    def go(self):
        self.logService.track('VALIDATE')

        interval = self.dataInterface.configGet('interval')
        symbols = self.dataInterface.configGet('symbols')
        for symbol in symbols:
            self.validateStockData(symbol, interval)

        self.logService.untrack('VALIDATE')


    def validateStockData(self, symbol, interval):
        self.stockDataInterface.load(interval, symbol)

        activeDateTime = datetime.strptime(self.stockDataInterface.next()[0],
                                           self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d' else
                                           self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        monthHolidayCountDirectory = dict(self.monthHolidayCountDirectory)
        activeYear = activeDateTime.year
        while self.stockDataInterface.next():
            # On a year change, reset month-holiday directory
            if activeDateTime.year != activeYear:
                activeYear = activeDateTime.year
                monthHolidayCountDirectory = dict(self.monthHolidayCountDirectory)

            # Not including holidays, determine the next expected date/time
            nextExpectedDateTime = self.getNextExpectedDateTime(interval, activeDateTime)

            # Observed next date/time
            nextDateTime = datetime.strptime(self.stockDataInterface.peek()[0],
                                             self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d' else
                                             self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

            # If there is a discrepancy, attribute it to a holiday. If no more holidays, report error
            if nextDateTime != nextExpectedDateTime:
                holidayCount = monthHolidayCountDirectory.get(nextExpectedDateTime.month)

                if holidayCount and holidayCount > 0:
                    monthHolidayCountDirectory.update({nextExpectedDateTime.month: holidayCount - 1})
                elif holidayCount and holidayCount <= 0:
                    self.logService.log('Missing data for {} ({}) on {}'.format(symbol, interval, nextExpectedDateTime))

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
