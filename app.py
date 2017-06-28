#!/usr/bin/env python

import csv
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('gamelog')
args = parser.parse_args()

wins = defaultdict(int)
opps = defaultdict(list)
teams = set()

# http://www.retrosheet.org/gamelogs/glfields.txt
for row in csv.reader(open(args.gamelog)):
    visitor = row[4-1]
    vscore = int(row[10-1])
    home = row[7-1]
    hscore = int(row[11-1])

    teams.add(home)
    teams.add(visitor)

    if hscore > vscore:
        wins[home] += 1
    elif vscore > hscore:
        wins[visitor] += 1

    opps[home].append(visitor)
    opps[visitor].append(home)

teams = sorted(teams)
ratings = {team: 100.0 for team in teams}
iterations = 0

while True:
    new_ratings = ratings.copy()
    delta = 0.0

    for team in teams:
        new_ratings[team] = wins[team] * sum(1 / (ratings[team] + ratings[opp]) for opp in opps[team]) ** -1
        delta += abs(new_ratings[team] - ratings[team])

    ratings = new_ratings.copy()

    if delta < 0.0001:
        break

    if iterations >= 5000:
        print '# breaking after %d iterations with delta = %.3f' % (iterations, delta)
        break

    iterations += 1

print '# %d iterations' % iterations
s = sorted(ratings.items(), key=lambda e: e[1], reverse=True)
for idx, (team, rating) in enumerate(s, 1):
    print (idx, team, round(rating, 3))

