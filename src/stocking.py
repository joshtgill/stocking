from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService
import traceback
from utility.email_interface import EmailInterface


class Stocking:

    def __init__(self, configPath):
        self.fileInterface = FileInterface()
        self.configInterface = ConfigInterface(configPath, self.fileInterface)
        self.logService = LogService(self.fileInterface)


    def start(self):
        self.logService.start('STOCKING')

        try:
            configServiceMap = {'queries': self.query, 'analyze': self.analyze}
            for serviceConfig in self.configInterface.get():
                self.configInterface.setScope(serviceConfig)

                configServiceMap.get(serviceConfig)()

                self.configInterface.setScope()
        except Exception:
            self.logService.log('STOCKING', traceback.format_exc(), 'ERROR')

        self.logService.stop('STOCKING')

        self.email()


    def query(self):
        for queryConfig in self.configInterface.get('queries'):
            self.logService.start('QUERY {}'.format(queryConfig.get('interval')))

            stockDataInterface = StockDataInterface(queryConfig.get('interval'))
            queryService = QueryService(queryConfig, stockDataInterface)
            queryService.start()

            self.logService.stop('QUERY {}'.format(queryConfig.get('interval')))


    def analyze(self):
        self.logService.start('ANALYZE')

        dayStockDataInterface = StockDataInterface('1d')
        analyzeService = AnalyzeService(self.configInterface, dayStockDataInterface, self.fileInterface)
        analyzeService.start()

        self.logService.stop('ANALYZE')


    def email(self):
        # Subject is based on if an error occurred
        emailSubject = 'Stocking COMPLETE\n'
        if self.logService.errorOccurred:
            emailSubject = 'Stocking FAILED\n'

        # Email body consists of services initiated and log text
        emailBody = ''

        # Display services initiated
        initiatedServices = 'Services initiated: '
        for i in range(len(self.configInterface.get('queries', []))):
            initiatedServices += 'QUERY {}'.format(self.configInterface.get('queries')[i])
            if i < len(self.configInterface.get('queries')) - 1:
                initiatedServices += ', '
        if self.configInterface.get('analyze'):
            initiatedServices += 'ANALYZE'
        emailBody += initiatedServices + '\n\n'

        # Display log text
        logText = ''
        with open(self.logService.logPath, 'r') as logFile:
            logText += logFile.read()
        emailBody += logText

        emailInterface = EmailInterface(self.fileInterface)
        emailInterface.sendEmail('joshtg.007@gmail.com', emailSubject, emailBody)
