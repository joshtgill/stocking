import json


class ConfigInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.configVarMap = {'ALL_SYMBOLS': 'exe/symbols/all_symbols.json'}


    def load(self, configPath):
        # Get general config
        config = json.loads(self.fileInterface.read(configPath))

        # Load stock symbols for declared services
        for queryConfig in config.get('queries'):
            self.loadStockSymbols(queryConfig)
        self.loadStockSymbols(config.get('analyze'))

        return config


    def loadStockSymbols(self, config):
        symbols = config.get('symbols')
        if not isinstance(symbols, list):
            if symbols in self.configVarMap.keys():  # Symbols value is config var
                symbols = json.loads(self.fileInterface.read(self.configVarMap.get(symbols)))
            else:  # Symbols value is a single symbol
                symbols = [symbols]
            config.update({'symbols': symbols})

        return config
