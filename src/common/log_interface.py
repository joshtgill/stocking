from collections import OrderedDict
from datetime import datetime


class LogInterface:

    def __init__(self, fileInterface, dataInterface):
        self.fileInterface = fileInterface
        self.dataInterface = dataInterface
        self.taskDir = OrderedDict()  # {name: start time}

        self.fileInterface.wipe(self.dataInterface.settingsGet('logPath'))


    def start(self, taskName):
        self.taskDir.update({taskName: datetime.now()})
        self.log('Started {}'.format(taskName), 'INFO')


    def stop(self, taskName):
        self.log('Completed {} in {}'.format(taskName, datetime.now() - list(self.taskDir.values())[-1]), 'INFO')
        self.taskDir.pop(taskName, None)


    def log(self, message, logType='INFO'):
        self.fileInterface.write(self.dataInterface.settingsGet('logPath'),
                                 '{} {}: {}\n'.format(datetime.now(), logType, message))
