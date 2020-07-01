from process.analyze.analyze_service import AnalyzeService


class ProcessService():

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService


    def go(self):
        for interval in self.configInterface.get():
            symbols = self.configInterface.get('{}/symbols'.format(interval))
            start = self.configInterface.get('{}/start'.format(interval))
            end = self.configInterface.get('{}/end'.format(interval))
            for module in self.configInterface.get('{}/modules'.format(interval)):
                self.logService.register(module)
                self.logService.log(module, 'Analyzing {}'.format(interval), 'info')
                AnalyzeService(interval, symbols, start, end).go()
                self.logService.unregister(module)
