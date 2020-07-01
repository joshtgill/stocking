from datetime import datetime


class LogService:

    def __init__(self, fileInterface):
        self.logPath = 'out/logs/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.fileInterface = fileInterface
        self.serviceStartDateTimes = {}
        self.errorOccurred = False


    def register(self, service):
        self.serviceStartDateTimes.update({service: datetime.now()})
        self.log(service, 'Started', 'info')


    def unregister(self, service):
        startDateTime = self.serviceStartDateTimes.get(service)
        self.log(service, 'Completed in {}'.format(datetime.now() - startDateTime), 'stat')


    def log(self, service, message, logType='info'):
        self.fileInterface.write(self.logPath, '[{}] ({}::{}): {}\n'.format(datetime.now(), logType.upper(), service.upper(), message))

        if logType == 'error':
            self.errorOccurred = True
