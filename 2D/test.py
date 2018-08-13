a = 'abcda'
for i in range(-1, len(a) - 2):
    print(a[1:][i],": ",[a[1:][i+k] for k in (-1, 0, 1)])
