class BaseService:

    def __init__(self, name, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface):
        self.name = name
        self.dataInterface = dataInterface
        self.logInterface = logInterface
        self.stockSymbolsInterface = stockSymbolsInterface
        self.stockHistoryInterface = stockHistoryInterface


    def start(self):
        self.logInterface.start(self.name)

        self.go()

        self.logInterface.stop(self.name)


    def translateConfigVariable(self, variable):
        if variable == 'NOW':
            return datetime.now().strftime(self.settingsGet('{}/dateTimeFormat'.format('1d')))
        elif 'NOW' in variable:
            openMarketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')).replace('d', ''))
            return self.determineDate(openMarketDaysBack).strftime(self.settingsGet('{}/dateTimeFormat'.format('1d')))

        return variable


    def determineDate(self, openMarketDaysBack):
        # 2020 stock market holiday closures
        marketClosedDates = [datetime(2020, 1, 1).date(), datetime(2020, 1, 20).date(), datetime(2020, 2, 17).date(),
                             datetime(2020, 4, 10).date(), datetime(2020, 5, 25).date(), datetime(2020, 7, 3).date(),
                             datetime(2020, 9, 7).date(), datetime(2020, 11, 26).date(), datetime(2020, 12, 25).date()]

        # Find the date associated with the number of market days back
        date = datetime.now().date()
        while True:
            if date.weekday() < 5 and date not in marketClosedDates:
                openMarketDaysBack -= 1

            if not openMarketDaysBack:
                break

            date = date - timedelta(days=1)

        return date
