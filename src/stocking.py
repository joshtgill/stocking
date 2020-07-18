from common.file_interface import FileInterface
from common.data_interface import DataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.process_service import ProcessService
from trade.trade_service import TradeService
import traceback
from utility.email_interface import EmailInterface
from datetime import datetime


class Stocking:

    def __init__(self, configPath, settingsPath):
        self.fileInterface = FileInterface()
        self.dataInterface = DataInterface(self.fileInterface, configPath, settingsPath)
        self.logService = LogService(self.fileInterface, self.dataInterface)
        self.tradeService = TradeService(self.dataInterface, self.logService, self.fileInterface)


    def go(self):
        self.logService.track('STOCKING')

        serviceDirectory = {'query': self.query, 'process': self.process, 'trade': self.trade}

        try:
            for service in self.dataInterface.configGet():
                # Set to service's config
                self.dataInterface.incrementConfig(service)

                # Start corresponding service
                serviceDirectory.get(service)()

                # Revert config to root config
                self.dataInterface.decrementConfig()
        except Exception:
            self.logService.log(traceback.format_exc(), 'ERROR')

        self.logService.untrack('STOCKING')

        self.email()


    def query(self):
        QueryService(self.dataInterface, self.logService).go()


    def process(self):
        ProcessService(self.dataInterface, self.logService, self.tradeService).go()


    def trade(self):
        self.tradeService.go()


    def email(self):
        logText = self.fileInterface.read(self.dataInterface.settingsGet('stockingLogPath'))

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
