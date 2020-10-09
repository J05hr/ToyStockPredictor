import csv
from typing import List


def formatdata(filename, train):
    rawList = []
    avgList = []
    featureList = []
    lastdate = ""
    try:
        # try to open the csv and read the raw data into a list of tuples
        with open(filename, "r") as dfile:
            csvr = csv.reader(dfile, delimiter=',')
            # skip the header
            next(csvr)
            for line in csvr:
                # small line length means theres an error
                if len(line) < 7:
                    raise Exception("number of columns in the csv is too small")
                rd = (float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[6]))
                lastdate = line[0]
                rawList.append(rd)

        # turn the raw data list into a feature list
        # features defined by a 5 day moving average of each days variables then transform to a % change per day
        for vidx in range(len(rawList)):
            # start avgs after we have enough history
            if vidx >= 4:
                f1, f2, f3, f4, f5 = 0, 0, 0, 0, 0
                # avg the 5 items
                for idx in range(vidx-4, vidx+1):
                    f1 += rawList[idx][0]
                    f2 += rawList[idx][1]
                    f3 += rawList[idx][2]
                    f4 += rawList[idx][3]
                    f5 += rawList[idx][4]
                # append the avgs to the feature list
                avgList.append((f1/5, f2/5, f3/5, f4/5, f5/5,))

        for aidx in range(len(avgList)):
            # start features after we have enough history to get a percent change
            if aidx >= 1:
                # get the precent change
                f1 = round((100 * rawList[aidx][0] / rawList[aidx-1][0]) - 100)
                f2 = round((100 * rawList[aidx][1] / rawList[aidx-1][1]) - 100)
                f3 = round((100 * rawList[aidx][2] / rawList[aidx-1][2]) - 100)
                f4 = round((100 * rawList[aidx][3] / rawList[aidx-1][3]) - 100)
                f5 = round((100 * rawList[aidx][4] / rawList[aidx-1][4]) - 100)
                # append the avgs to the feature list
                featureList.append((f1, f2, f3, f4, f5,))

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    return featureList, [False, filename, lastdate]

