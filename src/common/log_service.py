from datetime import datetime


class LogService:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.logPath = 'out/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.serviceStartDateTimes = {}
        self.errorOccurred = False


    def start(self, service):
        self.serviceStartDateTimes.update({service: datetime.now()})
        self.log(service, 'Started', 'STAT')


    def stop(self, service):
        startDateTime = self.serviceStartDateTimes.get(service)
        self.log(service, 'Completed in {}'.format(datetime.now() - startDateTime), 'STAT')


    def log(self, service, message, logType='INFO'):
        self.fileInterface.write(self.logPath, '[{}] ({}::{}): {}\n'.format(datetime.now(), logType, service, message))

        if logType == 'ERROR':
            self.errorOccurred = True
