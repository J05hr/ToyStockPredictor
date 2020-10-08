


def formatdata(filename):
    try:
        fle = open(filename, "r")
        countbig = 0
        sumbig = 0
        for lne in fle:
            fields = lne.split(" ")
            bytes = fields[6]
            if int(bytes) > 5000:
                countbig += 1
                sumbig += int(bytes)

        newfle = open("bytes_" + filename, "x")
        newfle.write(str(countbig) + " " + str(sumbig))
    except Exception:
        print("failed")


