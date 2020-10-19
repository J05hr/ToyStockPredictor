import csv
from objs.feature_vectors import FeatureVectors


def formatdata(filename, movingavgdays, outcomebasis):
    rawlist = []
    perclist = []  # percent change day to day
    avglist = []  # moving avg
    featurelist = []  # avglist but by percent change day to day
    outcomes = []  # buy, sell, or hold

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
                rawlist.append(rd)

        # turn the raw data list into a feature list
        # features defined by a moving average of each days variables
        for vidx in range(len(rawlist)):
            # start avgs after we have enough history
            if vidx >= movingavgdays-1:
                f1, f2, f3, f4, f5 = 0, 0, 0, 0, 0
                f0 = rawlist[vidx][0]
                # avg the 5 items
                for idx in range(vidx-(movingavgdays-1), vidx+1):
                    f1 += rawlist[idx][1]
                    f2 += rawlist[idx][2]
                    f3 += rawlist[idx][3]
                    f4 += rawlist[idx][4]
                    f5 += rawlist[idx][5]
                # append the avgs to the feature list
                avglist.append((f0, f1/movingavgdays, f2/movingavgdays, f3/movingavgdays, f4/movingavgdays, f5/movingavgdays))

        for aidx in range(len(avglist)):
            # start features after we have enough history to get a percent change
            if aidx >= 1:
                # get the percent change
                f0 = avglist[aidx][0]
                f1 = round((100 * avglist[aidx][1] / avglist[aidx-1][1]) - 100)
                f2 = round((100 * avglist[aidx][2] / avglist[aidx-1][2]) - 100)
                f3 = round((100 * avglist[aidx][3] / avglist[aidx-1][3]) - 100)
                f4 = round((100 * avglist[aidx][4] / avglist[aidx-1][4]) - 100)
                f5 = round((100 * avglist[aidx][5] / avglist[aidx-1][5]) - 100)
                # append the avgs to the feature list
                featurelist.append((f0, f1, f2, f3, f4, f5))

        # outcomes
        for vidx in range(len(rawlist)):
            # start features after we have enough history to get a percent change
            if vidx >= 1:
                # get the percent change
                f0 = rawlist[vidx][0]
                f1 = round((100 * rawlist[vidx][1] / rawlist[vidx - 1][1]) - 100)
                f2 = round((100 * rawlist[vidx][2] / rawlist[vidx - 1][2]) - 100)
                f3 = round((100 * rawlist[vidx][3] / rawlist[vidx - 1][3]) - 100)
                f4 = round((100 * rawlist[vidx][4] / rawlist[vidx - 1][4]) - 100)
                f5 = round((100 * rawlist[vidx][5] / rawlist[vidx - 1][5]) - 100)
                # append the avgs to the feature list
                perclist.append((f0, f1, f2, f3, f4, f5))

        # decisions based on close price of the next day, the outcome range is defined by the outcomebasis tuple
        # if the next day close is more than +x% then it was a buy
        # if it's between +x% and -y% it was a hold
        # if it's less than -y% then it was a sell
        for idx in range(len(perclist)-1):
            if perclist[idx+1][4] >= outcomebasis[0]:
                outcomes.append((perclist[idx][0], 'b'))
            elif perclist[idx+1][4] <= outcomebasis[1]:
                outcomes.append((perclist[idx][0], 's'))
            else:
                outcomes.append((perclist[idx][0], 'h'))

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    # return the arrays and trim so indexes match based on the moving average days
    rlst = movingavgdays
    plst = movingavgdays - 1
    olst = plst

    # featurelist will always have an additional item at the end which is used to make the final prediction
    return FeatureVectors(rawlist[rlst:-1], perclist[plst:-1], avglist[1:-1], featurelist, outcomes[olst:])

