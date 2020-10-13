from objs.feature_vectors import FeatureVectors
import core.featureextractor as featex
import core.naivebayes as nbayes
import math
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
    allfvs = featex.formatdata(filename, movingavgdays, outcomebasis)
    # get the total number of data points minus the last
    dcnt = len(allfvs.featurelist) - 1
    splitidx = math.ceil(dcnt * 0.9)
    # 90%/10% training/testing split
    trainfvs = FeatureVectors(allfvs.rawlist[:splitidx], allfvs.perclist[:splitidx], allfvs.avglist[:splitidx], allfvs.featurelist[:splitidx], allfvs.outcomes[:splitidx])
    testfvs = FeatureVectors(allfvs.rawlist[splitidx:], allfvs.perclist[splitidx:], allfvs.avglist[splitidx:], allfvs.featurelist[splitidx:], allfvs.outcomes[splitidx:])

    # figure out some basic training variables
    traindcnt = len(trainfvs.featurelist)  # num of features
    bcount = 0
    scount = 0
    hcount = 0
    for outcome in trainfvs.outcomes:
        if outcome[1] == 'b':
            bcount += 1
        elif outcome[1] == 's':
            scount += 1
        else:
            hcount += 1
    bprior = bcount / traindcnt
    sprior = scount / traindcnt
    hprior = hcount / traindcnt

    # train model to get a data set for P(data|results) and other probabilities needed for naive bayes
    td = nbayes.train(trainfvs.featurelist, trainfvs.outcomes, bcount, scount, hcount)

    # record the accuracy of the classification
    correctcnt = 0
    # loop through the testing data and do classification
    for fvidx in range(len(testfvs.featurelist)-1):
        featurevector = testfvs.featurelist[fvidx]
        # get evidence probability for this vector
        ev = nbayes.getevidence(featurevector, trainfvs.featurelist, traindcnt)
        res = nbayes.classify(featurevector, td, ev, bprior, sprior, hprior)
        # print the results
        print("  p(buy|data)    |     p(sell|data)    |     p(hold|data)")
        print(res)
        # figure out the predicted outcome
        if res.index(max(res)) == 0:
            pout = 'b'
        elif res.index(max(res)) == 1:
            pout = 's'
        else:
            pout = 'h'
        # check if the test prediction was accurate and print
        if testfvs.outcomes[fvidx][1] == pout:
            correctcnt += 1
            print("prediction correct\n")
        else:
            print("prediction incorrect\n")

    # print the accuracy of the classification at the end of testing
    accur = correctcnt / (len(testfvs.featurelist)-1)
    print("total prediction accuracy is: " + str(accur) + "\n")

    # take the most recent feature and run the model to predict the unknown decision
    lastvector = testfvs.featurelist[-1]
    ev = nbayes.getevidence(lastvector, trainfvs.featurelist, traindcnt)
    res = nbayes.classify(lastvector, td, ev, bprior, sprior, hprior)
    print("\nfinal prediction for the unknown last day")
    print("  p(buy|data)    |     p(sell|data)    |     p(hold|data)")
    print(str(res) + "\n")


if __name__ == '__main__':
    # print to the user
    print("\nJosh's toy stock predictor\n*")
    print("Outcome labels are based on close price of the next day.\n-If the next day close is more than +3% then it was a buy.\n"
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

