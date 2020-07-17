from collections import OrderedDict
from datetime import datetime


class LogService:

    def __init__(self, fileInterface, configInterface):
        self.fileInterface = fileInterface
        self.configInterface = configInterface
        self.taskDir = OrderedDict()  # {name: start time}

        self.fileInterface.wipe(self.configInterface.settingsGet('stockingLogPath'))


    def track(self, taskName):
        self.taskDir.update({taskName: datetime.now()})
        self.log('Started', 'INFO')


    def untrack(self, taskName):
        self.log('Completed in {}'.format(datetime.now() - list(self.taskDir.values())[-1]), 'STAT')
        self.taskDir.pop(taskName, None)


    def log(self, message, logType='INFO'):
        self.fileInterface.write(self.configInterface.settingsGet('stockingLogPath'),
                                 '[{}] ({}::{}): {}\n'.format(datetime.now(), logType, list(self.taskDir.keys())[-1], message))
