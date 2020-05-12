import json


class ConfigInterface:

    def __init__(self, mainConfigFilePath, fileService):
        self.fileService = fileService
        self.mainConfig = self.loadConfig(mainConfigFilePath)
        self.queryConfig = self.loadQueryConfig(self.mainConfig.get('queryConfigFilePath'))
        self.tradeConfig = self.loadConfig(self.mainConfig.get('tradeConfigFilePath'))


    def loadConfig(self, configFilePath):
        return json.loads(self.fileService.read(configFilePath))


    def loadQueryConfig(self, configFilePath):
        config = json.loads(self.fileService.read(configFilePath))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}

        # TODO: Generalize for any config structure
        for interval, intervalData in config.get('queries').items():
            symbols = intervalData.get('symbols')
            if not isinstance(symbols, list):
                if symbols in configVarMap.keys():  # Symbols value is config var
                    symbolsData = json.loads(self.fileService.read(configVarMap.get(symbols)))
                else:  # Symbols value is a single symbol
                    symbolsData = [symbols]
                intervalData.update({'symbols': symbolsData})

        return config
