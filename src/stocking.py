from common.file_interface import FileInterface
from common.data_interface import DataInterface
from common.log_interface import LogInterface
from common.stock_symbols_interface import StockSymbolsInterface
from common.stock_history_interface import StockHistoryInterface
from common.stock_splits_interface import StockSplitsInterface
from query.query_service import QueryService
from process.validate.validate_service import ValidateService
from process.process_service import ProcessService
from process.analyze.day_analyze_service import DayAnalyzeService
from process.analyze.minute_analyze_service import MinuteAnalyzeService
from trade.trade_service import TradeService
from display.display_service import DisplayService
import traceback
from datetime import datetime


class Stocking:

    def __init__(self, configPath, settingsPath):
        self.fileInterface = FileInterface()
        self.dataInterface = DataInterface(self.fileInterface, configPath, settingsPath)
        self.logInterface = LogInterface(self.fileInterface, self.dataInterface)
        self.stockSymbolsInterface = StockSymbolsInterface(self.dataInterface, self.logInterface)
        self.stockHistoryInterface = StockHistoryInterface({'day': self.dataInterface.settingsGet('day/stockHistoryPath'),
                                                            'minute': self.dataInterface.settingsGet('minute/stockHistoryPath')})
        self.stockSplitsInterface = StockSplitsInterface(self.dataInterface.settingsGet('stockSplitsPath'))
        self.queryService = QueryService(self.dataInterface, self.logInterface, self.stockSymbolsInterface,
                                         self.stockHistoryInterface, self.stockSplitsInterface)
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
