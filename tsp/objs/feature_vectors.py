

class FeatureVectors:

    def __init__(self, rawlist, perclist, avglist, featurelist, outcomes):

        self.rawlist = rawlist  # raw data in a list of tuples
        self.perclist = perclist  # percent change day to day
        self.avglist = avglist  # moving avg list
        self.featurelist = featurelist  # moving average then transformed to percent change day to day
        self.outcomes = outcomes  # array of buy, sell, or hold
