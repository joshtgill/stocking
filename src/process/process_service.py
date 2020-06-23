from process.analyze.analyze_service import AnalyzeService


class ProcessService():

    def __init__(self, configInterface):
        self.configInterface = configInterface


    def start(self):
        for interval in self.configInterface.get():
            symbols = self.configInterface.get('{}/symbols'.format(interval))
            if 'analyze' in self.configInterface.get('{}/services'.format(interval)):
                analyzeService = AnalyzeService(interval, symbols)
                analyzeService.start()
