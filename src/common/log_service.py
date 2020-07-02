from datetime import datetime


class LogService:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.serviceStartDateTimes = {}
        self.errorOccurred = False

        self.fileInterface.wipe('out/stocking.log')


    def register(self, service):
        self.serviceStartDateTimes.update({service: datetime.now()})
        self.log(service, 'Started', 'info')


    def unregister(self, service):
        startDateTime = self.serviceStartDateTimes.get(service)
        self.log(service, 'Completed in {}'.format(datetime.now() - startDateTime), 'stat')


    def log(self, service, message, logType='info'):
        self.fileInterface.write('out/stocking.log', '[{}] ({}::{}): {}\n'.format(datetime.now(),
                                                                                  logType.upper(),
                                                                                  service.upper(),
                                                                                  message))

        if logType == 'error':
            self.errorOccurred = True
