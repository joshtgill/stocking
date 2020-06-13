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
        self.config = ConfigInterface(self.fileInterface).load(configPath)
        self.logService = LogService(self.fileInterface)


    def startServices(self):
        self.logService.start('STOCKING')

        # Start services based on config
        try:
            if 'queries' in self.config:
                self.query()
        except Exception as e:
            self.logService.log('STOCKING', traceback.format_exc(), 'ERROR')

        self.logService.stop('STOCKING')

        # Email results of run
        self.email()


    def query(self):
        for queryConfig in self.config.get('queries'):
            self.logService.start('QUERY {}'.format(queryConfig.get('interval')))

            # stockDataInterface = StockDataInterface(queryConfig.get('interval'))
            # queryService = QueryService(queryConfig, stockDataInterface)
            # queryService.start()

            self.logService.stop('QUERY {}'.format(queryConfig.get('interval')))


    def analyze(self):
        pass


    def email(self):
        # Subject is based on if an error occurred
        emailSubject = 'Stocking COMPLETE\n'
        if self.logService.errorOccurred:
            emailSubject = 'Stocking FAILED\n'

        # Email body consists of services initiated and log text
        emailBody = ''
        # Display services initiated
        initiatedServices = 'Services initiated: '
        for queryConfig in self.config.get('queries'):
            initiatedServices += 'QUERY {}, '.format(queryConfig.get('interval'))
        emailBody += initiatedServices[: -2] + '\n'
        # Display log text
        logText = 'Log:\n'
        with open(self.logService.logPath, 'r') as logFile:
            logText += logFile.read()
        emailBody += logText

        emailInterface = EmailInterface(self.fileInterface)
        emailInterface.sendEmail('joshtg.007@gmail.com', emailSubject, emailBody)
