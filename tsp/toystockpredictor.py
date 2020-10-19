from objs.feature_vectors import FeatureVectors
import core.featureextractor as featex
import core.naivebayes as nbayes
from pathlib import Path
import math
import os
import re


# boolean to tell us if we've trained yet
trained = [False, "none", "none"]
# exit condition
done = False


def getcommands():
    # variable for the moving average
    print("How long would you like the moving average to be in days?  eg: 5")
    mad = input("Input a number : ")
    while not re.search("^(\\d+)$", mad) or 0 > int(mad) > 500:
        print("Invalid moving average quantity")
        mad = input("Input a number : ")
    print("*")

    # basis for defining the outcomes, a tuple containing high low splits that decide buy, hold, sell
    print("Define the outcome decision range.")
    ob1 = input("Input the percent gain above which to buy : ")
    while not re.search("^(\\d+)$", ob1) or 0 > int(ob1) > 500:
        print("Invalid positive range.")
        ob1 = input("Input the percent gain above which to buy : ")
    ob2 = input("Input the percent loss below which to sell : ")
    while not re.search("^(-\\d+)$", ob2) or 0 < int(ob2) or -500 > int(ob2) or int(ob1) == int(ob2):
        print("Invalid negative range.")
        ob2 = input("Input the percent loss below which to sell : ")
    print("*")
    print("Using range (%s, %s)\n*" % (ob1, ob2))

    # get filename to use
    print("Input a stock ticker. The model will be trained and applied to the last recorded day")
    fin = input("Which ticker would you like use?  eg: TSLA : ")
    path = str(Path.cwd()) + "\\data\\"
    while not os.path.isfile(path + fin.upper() + ".csv"):
        print("invalid filename.")
        fin = input("What file would you like use? (filename.csv) : ")

    fname = (path + fin.upper() + ".csv")
    movingavgd = int(mad)
    outcomeb = (int(ob1), int(ob2))

    return fname, movingavgd, outcomeb


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
    monin = 0
    monout = 0
    buyin = 0

    # loop through the testing data and do classification
    for fvidx in range(len(testfvs.featurelist)-2):
        featurevector = testfvs.featurelist[fvidx]
        # get evidence probability for this vector
        ev = nbayes.getevidence(featurevector, trainfvs.featurelist, traindcnt)
        res = nbayes.classify(featurevector, td, ev, bprior, sprior, hprior)
        # print the results
        print(featurevector[0])
        print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
        print(res)
        # figure out the predicted outcome
        if res.index(max(res)) == 0:
            pout = 'b'
            monin += 100
            buyin += 100
        elif res.index(max(res)) == 1:
            pout = 's'
            if monin > 100:
                monin -= 100
                monout += 100
        else:
            pout = 'h'
        # check if the test prediction was accurate and print
        if testfvs.outcomes[fvidx][1] == pout:
            correctcnt += 1
            print("outcome: " + testfvs.outcomes[fvidx][1] + " ,  prediction: " + pout + " ,  Correct\n")
        else:
            print("outcome: " + testfvs.outcomes[fvidx][1] + " ,  prediction: " + pout + " ,  I5ncorrect\n")

        percnextdayclose = testfvs.perclist[fvidx+1][4]
        nextdayprofit = monin * (percnextdayclose/100)
        monin += nextdayprofit

    # print the accuracy of the classification at the end of testing
    accur = correctcnt / (len(testfvs.featurelist)-1)
    print("total prediction accuracy is: " + str(accur * 100) + "%")
    print("money in: $" + str(monin) + ", money out: $" + str(monout))
    print("total buy in: $" + str(buyin) + ", profit: $" + str(monin + monout - buyin))

    # take the most recent feature and run the model to predict the unknown decision
    lastvector = testfvs.featurelist[-1]
    ev = nbayes.getevidence(lastvector, trainfvs.featurelist, traindcnt)
    res = nbayes.classify(lastvector, td, ev, bprior, sprior, hprior)
    print("\nfinal prediction for the unknown (last day)")
    print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
    print(str(res) + "\n")


if __name__ == '__main__':
    # print to the user
    print("\nJosh's toy stock predictor\n*")
    print("Outcome labels are based on close price of the next day.\n*\n*")

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

