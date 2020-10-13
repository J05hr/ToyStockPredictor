

class TrainingData:

    def __init__(self, numfeat):
        # each item is an array of feature dictionaries
        # keys correspond to feature values and values correspond to probabilities
        self.pbuys = []  # array for buys
        self.psells = []  # array for sells
        self.pholds = []  # array for holds
        # add the dictionaries for the number of features we have
        for idx in range(numfeat):
            self.pbuys.append(dict())
            self.psells.append(dict())
            self.pholds.append(dict())
