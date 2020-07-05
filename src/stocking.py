from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.process_service import ProcessService
import traceback
from utility.email_interface import EmailInterface
from datetime import datetime


class Stocking:

    def __init__(self, configPath, settingsPath):
        self.fileInterface = FileInterface()
        self.configInterface = ConfigInterface(self.fileInterface, configPath, settingsPath)
        self.logService = LogService(self.fileInterface, self.configInterface)


    def go(self):
        self.logService.register('stocking')

        serviceDirectory = {'query': self.query, 'process': self.process}

        try:
            for service in self.configInterface.configGet():
                self.logService.register(service)

                # Set to service's config
                self.configInterface.setConfig(service)

                # Start corresponding service
                serviceDirectory.get(service)()

                # Revert config to root config
                self.configInterface.resetConfig()

                self.logService.unregister(service)
        except Exception:
            self.logService.log('stocking', traceback.format_exc(), 'error')

        self.logService.unregister('stocking')

        self.email()


    def query(self):
        QueryService(self.configInterface, self.logService).go()


    def process(self):
        ProcessService(self.configInterface, self.logService).go()


    def email(self):
        logText = self.fileInterface.read(self.configInterface.settingsGet('stockingLogPath'))

        # Subject contains completion station and total run time
        totalRunTime = datetime.strptime(logText.split()[-1], '%H:%M:%S.%f')
        emailSubject = 'Stocking COMPLETE in' if not self.logService.errorOccurred else 'Stocking FAILED in'
        if totalRunTime.hour:
            emailSubject += '{} hours'.format(totalRunTime.hour)
        emailSubject += ' {} minutes'.format(totalRunTime.minute)

        # Body containts services initiated
        initiatedServices = []
        for interval in self.configInterface.configGet('query/queries', []):
            initiatedServices.append('Query {}'.format(interval))
        if self.configInterface.configGet('analyze'):
            initiatedServices.append('Analyze')
        emailBody = 'Services ran: ' + ', '.join(initiatedServices) +' \n\n'

        # Body contains log text
        emailBody += 'Log:\n' + logText

        EmailInterface(self.fileInterface, self.configInterface).buildEmail(emailSubject, emailBody)
