from common.file_interface import FileInterface
from common.data_interface import DataInterface
from common.log_interface import LogInterface
from common.stock_symbols_interface import StockSymbolsInterface
from common.stock_history_interface import StockHistoryInterface
from query.query_service import QueryService
from process.validate.validate_service import ValidateService
from process.process_service import ProcessService
from process.analyze.day_analyze_service import DayAnalyzeService
from process.analyze.minute_analyze_service import MinuteAnalyzeService
from trade.trade_service import TradeService
from display.display_service import DisplayService
import traceback
from datetime import datetime
from utility.email_interface import EmailInterface


class Stocking:

    def __init__(self, configPath, settingsPath):
        self.fileInterface = FileInterface()
        self.dataInterface = DataInterface(self.fileInterface, configPath, settingsPath)
        self.logInterface = LogInterface(self.fileInterface, self.dataInterface)
        self.stockSymbolsInterface = StockSymbolsInterface(self.dataInterface, self.logInterface)
        self.stockHistoryInterface = StockHistoryInterface({'day': self.dataInterface.settingsGet('day/stockHistoryPath'),
                                                            'minute': self.dataInterface.settingsGet('minute/stockHistoryPath')})
        self.queryService = QueryService(self.dataInterface, self.logInterface,
                                         self.stockSymbolsInterface, self.stockHistoryInterface)
        self.validateService = ValidateService(self.dataInterface, self.logInterface,
                                               self.stockSymbolsInterface, self.stockHistoryInterface)
        self.dayAnalyzeService = DayAnalyzeService(self.dataInterface, self.logInterface,
                                                   self.stockSymbolsInterface, self.stockHistoryInterface)
        self.minuteAnalyzeService = MinuteAnalyzeService(self.dataInterface, self.logInterface,
                                                         self.stockSymbolsInterface, self.stockHistoryInterface,
                                                         self.dayAnalyzeService)
        self.processService = ProcessService(self.dataInterface, self.logInterface,
                                             self.stockSymbolsInterface, self.stockHistoryInterface,
                                             self.dayAnalyzeService, self.minuteAnalyzeService)
        self.tradeService = TradeService(self.dataInterface, self.logInterface,
                                         self.stockSymbolsInterface, self.stockHistoryInterface,
                                         self.fileInterface, self.processService)
        self.displayService = DisplayService(self.dataInterface, self.logInterface,
                                             self.stockSymbolsInterface, self.stockHistoryInterface)


    def go(self, *args):
        self.logInterface.start('STOCKING')

        serviceDirectory = {'query': self.queryService, 'validate': self.validateService, 'process': self.processService,
                            'trade': self.tradeService, 'display': self.displayService}

        try:
            for i in range(len(self.dataInterface.configGet())):
                name = self.dataInterface.configGet('[{}]/name'.format(i))

                # Set to service's config
                self.dataInterface.incrementConfig('[{}]'.format(i))

                # Start corresponding service
                serviceDirectory.get(name).start()

                # Revert config to root config
                self.dataInterface.decrementConfig()
        except Exception:
            self.logInterface.log(traceback.format_exc(), 'ERROR')

        self.logInterface.stop('STOCKING')

        # self.email()


    def email(self):
        logText = self.fileInterface.read(self.dataInterface.settingsGet('logPath'))

        # Subject contains completion station and total run time
        totalRunTime = datetime.strptime(logText.split()[-1], '%H:%M:%S.%f')
        emailSubject = 'Stocking COMPLETE in' if 'ERROR' not in logText else 'Stocking FAILED in'
        if totalRunTime.hour:
            emailSubject += ' {} hours'.format(totalRunTime.hour)
        emailSubject += ' {} minutes'.format(totalRunTime.minute)

        # Body containts services initiated
        initiatedServices = []
        for interval in self.dataInterface.configGet('query/queries', []):
            initiatedServices.append('Query {}'.format(interval))
        if self.dataInterface.configGet('analyze'):
            initiatedServices.append('Analyze')
        emailBody = 'Services ran: ' + ', '.join(initiatedServices) +' \n\n'

        # Body contains log text
        emailBody += 'Log:\n' + logText

        EmailInterface(self.dataInterface, self.fileInterface).buildEmail(emailSubject, emailBody)
