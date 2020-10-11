import csv
from typing import List


def formatdata(filename):
    rawList = []
    percList = []  # percent change day to day
    avgList = []  # 5 day moving avg
    featureList = []  # avglist but by percent change day to day
    decisions = []  # buy, sell, or hold

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
                rd = (line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[6]))
                rawList.append(rd)

        # turn the raw data list into a feature list
        # features defined by a 5 day moving average of each days variables then transform to a % change per day
        for vidx in range(len(rawList)):
            # start avgs after we have enough history
            if vidx >= 2:
                f1, f2, f3, f4, f5 = 0, 0, 0, 0, 0
                f0 = rawList[vidx][0]
                # avg the 5 items
                for idx in range(vidx-2, vidx+1):
                    f1 += rawList[idx][1]
                    f2 += rawList[idx][2]
                    f3 += rawList[idx][3]
                    f4 += rawList[idx][4]
                    f5 += rawList[idx][5]
                # append the avgs to the feature list
                avgList.append((f0, f1/3, f2/3, f3/3, f4/3, f5/3))

        for aidx in range(len(avgList)):
            # start features after we have enough history to get a percent change
            if aidx >= 1:
                # get the percent change
                f0 = round((100 * avgList[aidx][1] / avgList[aidx-1][1]) - 100)
                f1 = round((100 * avgList[aidx][2] / avgList[aidx-1][2]) - 100)
                f2 = round((100 * avgList[aidx][3] / avgList[aidx-1][3]) - 100)
                f3 = round((100 * avgList[aidx][4] / avgList[aidx-1][4]) - 100)
                f4 = round((100 * avgList[aidx][5] / avgList[aidx-1][5]) - 100)
                # append the avgs to the feature list
                featureList.append((f0, f1, f2, f3, f4))

        # decisions
        for vidx in range(len(rawList)):
            # start features after we have enough history to get a percent change
            if vidx >= 1:
                # get the percent change
                f0 = round((100 * rawList[vidx][1] / rawList[vidx - 1][1]) - 100)
                f1 = round((100 * rawList[vidx][2] / rawList[vidx - 1][2]) - 100)
                f2 = round((100 * rawList[vidx][3] / rawList[vidx - 1][3]) - 100)
                f3 = round((100 * rawList[vidx][4] / rawList[vidx - 1][4]) - 100)
                f4 = round((100 * rawList[vidx][5] / rawList[vidx - 1][5]) - 100)
                # append the avgs to the feature list
                percList.append((f0, f1, f2, f3, f4))

        for idx in range(len(percList)-1):
            if idx >= 2:
                # decisions based on close price of the next day
                # if the next day close is more than +3% then it was a buy
                # if it's between +3% and -3% it was a hold
                # if it's less than -3% then it was a sell
                if percList[idx][4] > 3:
                    decisions.append('b')
                elif percList[idx][4] < -1:
                    decisions.append('s')
                else:
                    decisions.append('h')

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    return decisions, percList[3:]

