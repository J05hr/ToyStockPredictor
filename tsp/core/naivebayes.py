from objs.training_data import TrainingData


def train(trainingfvs, outcomes, bcount, scount,  hcount):
    # initialize
    numfeats = 6
    td = TrainingData(numfeats)

    # traverse the training outcomes and the training vectors at the same time and record data into td
    for idx in range(len(trainingfvs)):
        # choose the right outcome to record data for
        if outcomes[idx][1] == 'b':  # use td.pbuys
            for dctidx in range(1, numfeats):
                dct = td.pbuys[dctidx]
                featvalue = trainingfvs[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

        elif outcomes[idx][1] == 's':  # use td.psells
            for dctidx in range(1, numfeats):
                dct = td.psells[dctidx]
                featvalue = trainingfvs[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

        else:  # use td.pholds
            for dctidx in range(1, numfeats):
                dct = td.pholds[dctidx]
                featvalue = trainingfvs[idx][dctidx]
                try:
                    dct[featvalue] += 1
                except KeyError:
                    dct.setdefault(featvalue, 1)

    # for each array in td, replace counts with probabilities
    oarr = td.pbuys
    for dictidx in range(numfeats):
        dct = oarr[dictidx]
        for key in dct:
            vcount = dct[key]
            # divide total outcome count by the value count
            dct[key] = vcount / bcount
    oarr = td.psells
    for dictidx in range(numfeats):
        dct = oarr[dictidx]
        for key in dct:
            vcount = dct[key]
            # divide total outcome count by the value count
            dct[key] = vcount / scount
    oarr = td.pholds
    for dictidx in range(numfeats):
        dct = oarr[dictidx]
        for key in dct:
            vcount = dct[key]
            # divide total outcome count by the value count
            dct[key] = vcount / hcount

    return td


def getevidence(fv, trainingfvs, traincount):
    # loop through vectors and get counts for evidence probability
    # start with a very small count so the probability can't become 0 
    ep1 = 0.1
    ep2 = 0.1
    ep3 = 0.1
    ep4 = 0.1
    ep5 = 0.1
    for vector in trainingfvs:
        if vector[1] == fv[1]:
            ep1 += 1
        if vector[2] == fv[2]:
            ep2 += 1
        if vector[3] == fv[3]:
            ep3 += 1
        if vector[4] == fv[4]:
            ep4 += 1
        if vector[5] == fv[5]:
            ep5 += 1
    ev = (ep1 / traincount) * (ep2 / traincount) * (ep3 / traincount) * (ep4 / traincount) * (ep5 / traincount)
    return ev


def classify(fv, td, ev, bprior, sprior, hprior):
    pbuys = td.pbuys
    psells = td.psells
    pholds = td.pholds
    ev = 1/ev

    # smoothing value in case prob is 0
    smth = 0.01

    # calc p(data | result) for each outcome
    pdb = pholds[1].get(fv[1], smth) * pholds[2].get(fv[2], smth) * pbuys[3].get(fv[3], smth) * pbuys[4].get(fv[4], smth) * pbuys[5].get(fv[5], smth)
    pds = psells[1].get(fv[1], smth) * psells[2].get(fv[2], smth) * psells[3].get(fv[3], smth) * psells[4].get(fv[4], smth) * psells[5].get(fv[5], smth)
    pdh = pholds[1].get(fv[1], smth) * pholds[2].get(fv[2], smth) * pholds[3].get(fv[3], smth) * pholds[4].get(fv[4], smth) * pholds[5].get(fv[5], smth)

    # calc final probabilities
    pbd = pdb*bprior
    psd = pds*sprior
    phd = pdh*hprior

    norm = pdb + psd + phd

    # result is a tuple of ( p(buy|data), p(sell|data), p(hold|data) )
    res = [pbd/norm, psd/norm, phd/norm]

    return res


