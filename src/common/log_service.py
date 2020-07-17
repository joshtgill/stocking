from datetime import datetime


class LogService:

    def __init__(self, fileInterface, configInterface):
        self.fileInterface = fileInterface
        self.configInterface = configInterface
        self.taskDir = []  # [(name, start datetime)]

        self.fileInterface.wipe(self.configInterface.settingsGet('stockingLogPath'))


    def track(self, taskName):
        self.taskDir.append((taskName, datetime.now()))
        self.log('Started', 'INFO')


    def untrack(self, taskName):
        self.log('Completed in {}'.format(datetime.now() - self.taskDir[-1][1]), 'STAT')
        del self.taskDir[-1]


    def log(self, message, logType='INFO'):
        self.fileInterface.write(self.configInterface.settingsGet('stockingLogPath'),
                                 '[{}] ({}::{}): {}\n'.format(datetime.now(), logType, self.taskDir[-1][0], message))
