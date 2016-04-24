import csv
import json

def createTilesJson():
    f = open('data/letter_frequency.csv')
    rdr = csv.reader(f)
    freq = {}
    for row in rdr:
        freq[row[0]] = int(row[1])

    f2 = open('data/scores.csv')
    rdr = csv.reader(f2)
    scores = {}
    for row in rdr:
        scores[row[1]] = int(row[0])
    tiles = {'scores': scores, 'freq': freq}
    w = open('data/tiles.json', 'w')
    json.dump(tiles,w)

if __name__ == '__main__':
    createTilesJson()
