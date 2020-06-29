from process.analyze.analyze_service import AnalyzeService


class ProcessService():

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService


    def start(self):
        for interval in self.configInterface.get():
            symbols = self.configInterface.get('{}/symbols'.format(interval))
            startt = self.configInterface.get('{}/start'.format(interval))
            end = self.configInterface.get('{}/end'.format(interval))
            for module in self.configInterface.get('{}/modules'.format(interval)):
                self.logService.start(module)
                self.logService.log(module, 'Analyzing {}'.format(interval), 'info')
                analyzeService = AnalyzeService(interval, symbols, startt, end)
                analyzeService.startt()
                self.logService.stop(module)
