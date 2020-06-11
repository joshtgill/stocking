import json


class ConfigInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}


    def load(self, configPath):
        # Get general config
        config = json.loads(self.fileInterface.read(configPath))

        for queryConfig in config.get('queries'):
            self.loadSymbols(queryConfig)

        return config


    def loadSymbols(self, queryConfig):
        symbols = queryConfig.get('symbols')
        if not isinstance(symbols, list):
            if symbols in self.configVarMap.keys():  # Symbols value is config var
                symbols = json.loads(self.fileInterface.read(self.configVarMap.get(symbols)))
            else:  # Symbols value is a single symbol
                symbols = [symbols]
            queryConfig.update({'symbols': symbols})

        return queryConfig
