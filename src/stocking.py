from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService
import traceback
from utility.email_interface import EmailInterface


class Stocking:

    def __init__(self, configPath):
        self.fileInterface = FileInterface()
        self.logService = LogService(self.fileInterface)
        self.configInterface = ConfigInterface(configPath, self.fileInterface)


    def start(self):
        self.logService.start('stocking')

        serviceDirectory = {'query': self.query, 'analyze': self.analyze}

        try:
            for service in self.configInterface.get():
                self.logService.start(service)

                # Set to service's config
                self.configInterface.setConfig(service)

                # Start corresponding service
                serviceDirectory.get(service)()

                # Revert confg to root config
                self.configInterface.resetConfig()

                self.logService.stop(service)
        except Exception:
            self.logService.log('stocking', traceback.format_exc(), 'error')

        self.logService.stop('stocking')

        self.buildEmail()


    def query(self):
        QueryService(self.configInterface).start()


    def analyze(self):
        AnalyzeService(self.configInterface, self.fileInterface).start()


    def buildEmail(self):
        # Subject is based on if an error occurred
        emailSubject = 'Stocking COMPLETE\n'
        if self.logService.errorOccurred:
            emailSubject = 'Stocking FAILED\n'

        # Email body consists of services initiated and log text
        emailBody = ''

        # Display services initiated
        initiatedServices = 'Services initiated: '
        for i in range(len(self.configInterface.get('queries', []))):
            initiatedServices += 'QUERY {}'.format(self.configInterface.get('queries')[i].get('interval'))
            if i < len(self.configInterface.get('queries')) - 1:
                initiatedServices += ', '
        if self.configInterface.get('analyze'):
            initiatedServices += ', ANALYZE'
        emailBody += initiatedServices + '\n\n'

        # Display log text
        logText = ''
        with open(self.logService.logPath, 'r') as logFile:
            logText += logFile.read()
        emailBody += logText

        EmailInterface(self.fileInterface).sendEmail('joshtg.007@gmail.com', emailSubject, emailBody)
