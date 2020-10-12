from objs.feature_vectors import FeatureVectors
import core.featureextractor as featex
import core.naivebayes as nbayes
import os


# boolean to tell us if we've trained yet
trained = [False, "none", "none"]
# exit condition
done = False


def getcommands():
    # print to the user
    print("Input a filename and the model will be trained and applied to the last line (current decision.\n*")
    fin = input("What file would you like use? (filename.csv) : ")
    path = 'C:/Users/J05h/Desktop/Projects/ToyStockPredictor/tsp/data/'
    while not os.path.isfile(path + fin):
        print("invalid filename.")
        fin = input("What file would you like use? (filename.csv) : ")

    # variable for the moving average
    movingavgdays = 0
    # basis for defining the outcomes, a tuple containing high low splits that decide buy, hold, sell
    outcomebasis = (2, -2)

    return path + fin, movingavgdays, outcomebasis


def run(filename, movingavgdays, outcomebasis):

    # get feature and outcomes data as a FeatureVectors object
    allfeaturevectors = featex.formatdata(filename, movingavgdays, outcomebasis)

    # 75%/25% training/testing split
    trainingfeaturevectors = FeatureVectors(rawlist, perclist, avglist, featurelist, outcomes)
    testingfeaturevectors = FeatureVectors(rawlist, perclist, avglist, featurelist, outcomes)

    # figure out some basic variables
    datacount = len(trainingfeaturevectors.featurelist - 1)  # num of features minus the last
    bcount = trainingfeaturevectors.outcomes.count('b')
    scount = trainingfeaturevectors.outcomes.count('s')
    hcount = len(trainingfeaturevectors.featurelist - 1) - bcount + scount
    bprior = bcount / datacount
    sprior = scount / datacount
    hprior = hcount / datacount

    # train model to get a data set for P(data|results) and other probabilities needed for naive bayes
    td = nbayes.train(trainingfeaturevectors.featurelist, trainingfeaturevectors.outcomes, bcount, scount, hcount)

    # record the accuracy of the classification

    # loop through the testing data and do classification
    for featurevector in testingfeaturevectors.featurelist[:-1]:
        # get evidence probability for this vector
        ev = nbayes.getevidence(featurevector, testingfeaturevectors.featurelist, datacount)
        res = nbayes.classify(featurevector, td, ev, bprior, sprior, hprior)
        print("\np(buy|data), p(sell|data), p(hold|data)")
        print(res)

    # take the most recent feature and run the model to predict the unknown decision
    lastVector = testingfeaturevectors.featurelist[-1]
    res = nbayes.classify(lastVector, td, bprior, sprior, hprior)
    print("\np(buy|data), p(sell|data), p(hold|data)")
    print(res)


if __name__ == '__main__':
    # print to the user
    print("\nJosh's toy stock predictor\n*")
    print("Decision labels are based on close price of the next day.\n-If the next day close is more than +3% then it was a buy.\n"
          "-If it's between +3% and -3% it was a hold.\n-If it's less than -3% then it was a sell.\n*\n*\n*")
    data = None

    while not done:

        # Read commands
        filename, movingavgdays, outcomebasis = getcommands()

        # Run the training or classification
        run(filename, movingavgdays, outcomebasis)

        # check if we are done
        d = input("Continue or exit? (C or X) : ")
        while d != "C" and d != "X":
            print("invalid option.")
            d = input("Continue or exit? (C or X) : ")
        done = (d == "X")

