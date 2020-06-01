from datetime import datetime


class LogService:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.logPath = 'log/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.startDateTime = None


    def start(self):
        self.startDateTime = datetime.now()


    def stop(self):
        self.log('Completed in {}'.format(datetime.now() - self.startDateTime), 'STAT')


    def log(self, message, logType='INFO'):
        self.fileInterface.write(self.logPath, '[{}] ({}): {}\n'.format(datetime.now(), logType, message))
