import json


class ConfigInterface:

    def __init__(self, mainConfigPath, fileService):
        self.fileService = fileService
        self.mainConfig = self.loadConfig(mainConfigPath)
        self.queryConfig = self.loadQueryConfig(self.mainConfig.get('queryConfigPath'))
        self.tradeConfig = self.loadConfig(self.mainConfig.get('tradeConfigPath'))


    def loadConfig(self, configPath):
        return json.loads(self.fileService.read(configPath))


    def loadQueryConfig(self, configPath):
        config = json.loads(self.fileService.read(configPath))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}
        for interval, intervalData in config.get('queries').items():
            symbolsValue = intervalData.get('symbols')
            if not isinstance(symbolsValue, list):
                if symbolsValue in configVarMap.keys():  # Symbols value is config var
                    symbolsData = json.loads(self.fileService.read(configVarMap.get(symbolsValue)))
                else:  # Symbols value is a single symbol
                    symbolsData = [symbolsValue]
                intervalData.update({'symbols': symbolsData})

        return config
