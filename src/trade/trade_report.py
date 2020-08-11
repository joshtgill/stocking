import json


class TradeReport:

    def __init__(self, averageGrowthPercent, percentRed):
        self.averageGrowthPercent = averageGrowthPercent
        self.percentRed = percentRed


    def serialize(self):
        data = {'averageGrowthPercent': self.averageGrowthPercent, 'percentRed': self.percentRed}

        return json.dumps(data)
