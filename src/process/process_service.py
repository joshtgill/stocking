from process.analyze.analyze_service import AnalyzeService


class ProcessService():

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService


    def start(self):
        for service in self.configInterface.get():
            self.logService.start(service)
            symbols = self.configInterface.get('{}/symbols'.format(service))
            for interval in self.configInterface.get('{}/intervals'.format(service)):
                self.logService.log(service, 'Analyzing {}'.format(interval), 'info')
                analyzeService = AnalyzeService(interval, symbols)
            self.logService.stop(service)
