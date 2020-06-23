from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.process_service import ProcessService
import traceback
from utility.email_interface import EmailInterface


class Stocking:

    def __init__(self, configPath):
        self.fileInterface = FileInterface()
        self.logService = LogService(self.fileInterface)
        self.configInterface = ConfigInterface(configPath, self.fileInterface)


    def start(self):
        self.logService.start('stocking')

        serviceDirectory = {'query': self.query, 'process': self.process}

        try:
            for service in self.configInterface.get():
                self.logService.start(service)

                # Set to service's config
                self.configInterface.setConfig(service)

                # Start corresponding service
                serviceDirectory.get(service)()

                # Revert config to root config
                self.configInterface.resetConfig()

                self.logService.stop(service)
        except Exception:
            self.logService.log('stocking', traceback.format_exc(), 'error')

        self.logService.stop('stocking')

        self.email()


    def query(self):
        QueryService(self.configInterface, self.logService).start()


    def process(self):
        ProcessService(self.configInterface, self.logService).start()


    def email(self):
        # Subject is based on whether an error occurred
        emailSubject = 'Stocking COMPLETE' if not self.logService.errorOccurred else 'Stocking FAILED'

        # Body containts services initiated
        initiatedServices = []
        for queryConfig in self.configInterface.get('query/queries', []):
            initiatedServices.append('Query {}'.format(queryConfig.get('interval')))
        if self.configInterface.get('analyze'):
            initiatedServices.append('Analyze')
        emailBody = 'Services ran: ' + ', '.join(initiatedServices) +' \n\n'

        # Body contains log text
        emailBody += 'Log:\n' + self.fileInterface.read(self.logService.logPath)

        EmailInterface(self.fileInterface).buildEmail(emailSubject, emailBody)
