from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.process_service import ProcessService
import traceback
from utility.email_interface import EmailInterface


class Stocking:

    def __init__(self, configPath):
        self.logService = LogService()
        self.fileInterface = FileInterface()
        self.configInterface = ConfigInterface(configPath, self.fileInterface)


    def go(self):
        self.logService.register('stocking')

        serviceDirectory = {'query': self.query, 'process': self.process}

        try:
            for service in self.configInterface.get():
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
        # Subject is based on whether an error occurred
        emailSubject = 'Stocking COMPLETE' if not self.logService.errorOccurred else 'Stocking FAILED'

        # Body containts services initiated
        initiatedServices = []
        for interval in self.configInterface.get('query/queries', []):
            initiatedServices.append('Query {}'.format(interval))
        if self.configInterface.get('analyze'):
            initiatedServices.append('Analyze')
        emailBody = 'Services ran: ' + ', '.join(initiatedServices) +' \n\n'

        # Body contains log text
        emailBody += 'Log:\n' + self.logService.logContent

        EmailInterface(self.fileInterface).buildEmail(emailSubject, emailBody)
