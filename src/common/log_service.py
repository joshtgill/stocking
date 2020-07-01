from datetime import datetime


class LogService:

    def __init__(self):
        self.logContent = ''
        self.serviceStartDateTimes = {}
        self.errorOccurred = False


    def register(self, service):
        self.serviceStartDateTimes.update({service: datetime.now()})
        self.log(service, 'Started', 'info')


    def unregister(self, service):
        startDateTime = self.serviceStartDateTimes.get(service)
        self.log(service, 'Completed in {}'.format(datetime.now() - startDateTime), 'stat')


    def log(self, service, message, logType='info'):
        self.logContent += '[{}] ({}::{}): {}\n'.format(datetime.now(), logType.upper(), service.upper(), message)

        if logType == 'error':
            self.errorOccurred = True
