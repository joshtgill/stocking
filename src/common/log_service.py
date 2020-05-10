from datetime import datetime


class LogService:

    def __init__(self):
        self.logFilePath = 'log/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.startDateTime = None


    def signalStart(self):
        self.startDateTime = datetime.now()


    def signalEnd(self):
        self.log('Completed in {}'.format(datetime.now() - self.startDateTime), 'STAT')


    def log(self, logMessage, logType='INFO'):
        logStr = '[{}] ({}): {}\n'.format(datetime.now(), logType, logMessage)
        with open(self.logFilePath, 'a+') as logFile:
            logFile.write(logStr)
