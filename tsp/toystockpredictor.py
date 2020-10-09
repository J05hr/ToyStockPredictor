
import core.featureextractor as featex
import core.naivebayes as nbayes
import os


# boolean to tell us if we've trained yet
trained = [False, "none", "none"]
# exit condition
done = False


def getcommands():
    # print to the user
    print(".\n    Input a filename to use. The model will be trained and applied to the last line (current decision")
    fin = input("   What file would you like use? (filename.csv) : ")
    path = 'C:/Users/J05h/Desktop/Projects/ToyStockPredictor/tsp/data/'
    while not os.path.isfile(path + fin):
        print("   invalid filename.\n.")
        fin = input("   What file would you like use? (filename.csv) : ")
    return path + fin


def run(fn):

    # get feature vectors and training info
    rawdata, featurevectors = featex.formatdata(filename, train)
    # train model
    trainingdata = nbayes.train(featurevectors)
    # take the most recent feature and run the model to predict the unknown decision
    lastVector = featurevectors[-1]
    # do classification
    res = nbayes.classify(lastVector)



if __name__ == '__main__':
    # print to the user
    print("\nJosh's toy stock predictor\n.")
    data = None

    while not done:

        # Read commands
        filename, train = getcommands()

        # Run the training or classification
        run(filename)

        # check if we are done
        d = input("    Continue or exit? (C or X) : ")
        while d != "C" and d != "X":
            print("    invalid option.\n")
            d = input("    Continue or exit? (C or X) : ")
        done = (d == "X")

