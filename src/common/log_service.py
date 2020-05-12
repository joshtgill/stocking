from datetime import datetime


class LogService:

    def __init__(self, fileService):
        self.fileService = fileService
        self.logFilePath = 'log/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.startDateTime = None


    def signalStart(self):
        self.startDateTime = datetime.now()


    def signalEnd(self):
        self.log('Completed in {}'.format(datetime.now() - self.startDateTime), 'STAT')


    def log(self, message, logType='INFO'):
        self.fileService.write(self.logFilePath, '[{}] ({}): {}\n'.format(datetime.now(), logType, message))
