import csv
import os

base = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
NAME = os.path.join(base, 'structural-connectivity-of-human-cerebral-cortex'
                    '-some-coordinates.csv')


# NOTE: not for all regions coordinates are available.

xyz = []
labels = []
with open(NAME) as f:
    for i, line in enumerate(csv.reader(f)):
        if i == 0:
            continue
        x, y, z, region = line
        xyz.append([int(x), int(y), int(z)])
        labels.append(region)
