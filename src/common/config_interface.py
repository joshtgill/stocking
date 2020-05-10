import json


class ConfigInterface:

    def __init__(self, mainConfigFilePath):
        self.mainConfig = self.loadConfig(mainConfigFilePath)

        self.queryConfig = self.loadQueryConfig(self.mainConfig.get('queryConfigFilePath'))
        self.tradeConfig = self.loadConfig(self.mainConfig.get('tradeConfigFilePath'))


    def loadConfig(self, configFilePath):
        return json.load(open(configFilePath, 'r'))


    def loadQueryConfig(self, configFilePath):
        config = json.load(open(configFilePath, 'r'))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}

        # TODO: Generalize for any config structure
        for interval, intervalData in config.get('queries').items():
            symbols = intervalData.get('symbols')
            if not isinstance(symbols, list):
                if symbols in configVarMap.keys():  # Symbols value is config var
                    symbolsData = json.load(open(configVarMap.get(symbols), 'r'))
                else:  # Symbols value is a single symbol
                    symbolsData = [symbols]
                intervalData.update({'symbols': symbolsData})

        return config
