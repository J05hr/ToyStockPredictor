
import core.featureextractor as featex
import os


# boolean to tell us if we've trained yet
trained = (False, "none")
# exit condition
done = False


def getCommands():
    # print to the user
    print("\n\n    Complete the options to run or train.\n\n")
    print("\n\n    Current training status: " + str(trained[0]) + ", file:" + trained[1] + "\n\n")
    # select training or application
    tin = input("    Would you like to train a model or apply it? (T or A) : ")
    while (tin == "A" and trained == False) or tin != "T" or tin != "A":
        if tin == "A":
            print("    Training hasn't been run yet, select training first\n")
            tin = input("    Would you like to train a model or apply it? (T or A) : ")
        else:
            print("    invalid option.\n")
            tin = input("    Would you like to train a model or apply it? (T or A) : ")
    # select file to run on
    if tin == "T":
        print("\n\n     Input a filename for training. "
              "The model will be trained on all data except the last line (current decision).")
    else:
        print("\n\n     Input a filename for application. The model will be applied to the last line (current decision")
    fin = input("    What file would you like use? (filename.csv) : ")
    while not os.path.isfile(fin):
        print("    invalid filename.\n")
        fin = input("    What file would you like use? (filename.csv) : ")

    return fin, tin == "T"


def run(fn, train):
    # if we need to do training
    if train:
        memes = 0
    # if we are just applying the model
    else:
        memes = 0


if __name__ == '__main__':
    # print to the user
    print("\n\nJosh's toy stock predictor\n\n")

    while not done:

        # Read commands
        filename, train = getCommands()

        # Run the application
        run(filename, train)

        # check if we are done
        d = input("    Continue or exit? (C or X) : ")
        while d != "C" or d != "X":
            print("    invalid option.\n")
            d = input("    Continue or exit? (C or X) : ")
        done = (d == "X")

