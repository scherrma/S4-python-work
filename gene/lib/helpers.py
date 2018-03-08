#csv functions
def opencsv(fname, headerlines=0, footerlines=0):
    data = []
    with open(fname, 'r') as fin:
        data = [l.strip().split(',') for l in fin if l.strip()]

    return data[headerlines: -footerlines if footerlines else None]

def writecsv(fname, data, header=()):
    with open(fname, 'w') as fout:
        if header:
            for elem in header[:-1]:
                fout.write(str(elem)+',')
            fout.write(str(header[-1])+'\n')

        for line in data:
            for elem in line[:-1]:
                fout.write(str(elem if elem != None else '')+',')
            fout.write(str(line[-1] if line[-1] != None else '')+'\n')
