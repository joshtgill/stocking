from datetime import datetime


class LogService:

    def __init__(self, fileInterface, configInterface):
        self.fileInterface = fileInterface
        self.configInterface = configInterface
        self.serviceDir = []  # [(name, start datetime)]

        self.fileInterface.wipe(self.configInterface.settingsGet('stockingLogPath'))


    def track(self, service):
        self.serviceDir.append((service, datetime.now()))
        self.log('Started', 'INFO')


    def untrack(self, service):
        self.log('Completed in {}'.format(datetime.now() - self.serviceDir[-1][1]), 'STAT')
        del self.serviceDir[-1]


    def log(self, message, logType='INFO'):
        self.fileInterface.write(self.configInterface.settingsGet('stockingLogPath'),
                                 '[{}] ({}::{}): {}\n'.format(datetime.now(), logType, self.serviceDir[-1][0], message))
