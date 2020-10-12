

def train(featurevectors, decisions, bcount, scount,  hcount):
    # initialize
    td = []
    # training data is a matrix of outcomes (x) arrays of feature dictionaries
    # td[0] is buy, td[1] is sell, td[2] is hold
    # keys correspond to feature values and values correspond to counts(transformed into probabilities at the end)
    for outcome in range(3):
        fv0 = dict()  # open
        fv1 = dict()  # high
        fv2 = dict()  # low
        fv3 = dict()  # close
        fv4 = dict()  # volume
        td.append([fv0, fv1, fv2, fv3, fv4])

    # traverse the decisions and feature vectors at the same time and record data into td
    for idx in range(len(featurevectors)-1):
        # choose the right outcome to record data for
        if decisions[idx] == 'b':  # use td[0]
            for dctidx in range(len(td[0])):
                dct = td[0][dctidx]
                featvalue = featurevectors[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

        elif decisions[idx] == 's':  # use td[1]
            for dctidx in range(len(td[1])):
                dct = td[2][dctidx]
                featvalue = featurevectors[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

        else:  # use td[2]
            for dctidx in range(len(td[2])):
                dct = td[2][dctidx]
                featvalue = featurevectors[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

    # loop through the td and generate probabilities
    for oarridx in range(len(td)):
        oarr = td[oarridx]
        for dictidx in range(len(oarr)):
            dct = oarr[dictidx]
            for key in dct:
                vcount = dct[key]
                # choose the right outcome to get a probability, divide total outcome count by the value count
                if oarridx == 0:  # use bcount
                    dct[key] = vcount / bcount
                elif oarridx == 1:  # use scount
                    dct[key] = vcount / scount
                else:  # use hcount
                    dct[key] = vcount / hcount

    return td


def classify(datacount, featurevectors, td, bprior, sprior, hprior):
    # take the most recent feature and run the model to predict the unknown decision
    lastVector = featurevectors[-1]
    # smoothing value in case prob is 0
    smth = 0.01
    # loop through vectors and get counts for evidence probability
    ep1 = 0
    ep2 = 0
    ep3 = 0
    ep4 = 0
    ep5 = 0
    for vector in featurevectors:
        if vector[0] == lastVector[0]:
            ep1 += 1
        if vector[1] == lastVector[1]:
            ep2 += 1
        if vector[2] == lastVector[2]:
            ep3 += 1
        if vector[3] == lastVector[3]:
            ep4 += 1
        if vector[4] == lastVector[4]:
            ep5 += 1
    ev = (ep1/datacount) * (ep2/datacount) * (ep3/datacount) * (ep4/datacount) * (ep5/datacount)

    # calc p(data | result) for each outcome
    pdb = td[0][0].get(lastVector[0], smth) * td[0][1].get(lastVector[1], smth) * td[0][2].get(lastVector[2], smth) * td[0][3].get(lastVector[3], smth) * td[0][4].get(lastVector[4], smth)
    pds = td[1][0].get(lastVector[0], smth) * td[1][1].get(lastVector[1], smth) * td[1][2].get(lastVector[2], smth) * td[1][3].get(lastVector[3], smth) * td[1][4].get(lastVector[4], smth)
    pdh = td[2][0].get(lastVector[0], smth) * td[2][1].get(lastVector[1], smth) * td[2][2].get(lastVector[2], smth) * td[2][3].get(lastVector[3], smth) * td[2][4].get(lastVector[4], smth)

    # calc final probabilities
    pbd = (1/ev)*pdb*bprior
    psd = (1/ev)*pds*sprior
    phd = (1/ev)*pdh*hprior

    # result is a tuple of ( p(buy|data), p(sell|data), p(hold|data) )
    res = [pbd, psd, phd]

    return res


