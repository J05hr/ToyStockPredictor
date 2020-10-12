
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
    return path + fin


def run(fn):

    # get feature vectors and training info
    decisions, featurevectors = featex.formatdata(filename)
    # figure out some basic variables
    datacount = len(featurevectors) - 1  # num of features minus the last
    bcount = decisions.count('b')
    scount = decisions.count('s')
    hcount = len(featurevectors) - bcount + scount
    bprior = bcount / datacount
    sprior = scount / datacount
    hprior = hcount / datacount
    # train model to get a data set for P(data|results) and other probabilities needed for naive bayes
    td = nbayes.train(featurevectors, decisions, bcount, scount, hcount)
    # do classification
    res = nbayes.classify(datacount, featurevectors, td, bprior, sprior, hprior)
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
        filename = getcommands()

        # Run the training or classification
        run(filename)

        # check if we are done
        d = input("Continue or exit? (C or X) : ")
        while d != "C" and d != "X":
            print("invalid option.")
            d = input("Continue or exit? (C or X) : ")
        done = (d == "X")

