import sys
import argparse
import json
import csv

from .models import RecommendationEngine
# from . import constants


def main(args=None):
    """Console script for eu2019model."""

    if args is None:
        update = True
        increment = 10000
        output = False
        risk = True
    else:
        update = args.update
        increment = args.increment
        output = args.output
        risk = args.defence

    data = []
    befores = []
    afters = []
    rec_parties = []
    engine = RecommendationEngine(increment, update)
    for region in engine.getAllRegions():
        rec = engine.recommendRegion(region, risk)
        if rec is not None:
            before, after, votes_taken, party = rec
            befores.append(before)
            afters.append(after)
            rec_parties.append(party)
            data.append(engine.toDict(before, after, party, votes_taken))

    # # Create csv file from data:
    with open('data/output.csv', 'w') as f:
        writer = csv.writer(f)
        tally = {}
        writer.writerow(["Pre-Simuation Results:"])
        for i, bef in enumerate(befores):
            lines, tally = bef.toCSV(i == 0, i == (len(befores)-1), tally)
            for l in lines:
                writer.writerow(l)
        writer.writerow([""])

        writer.writerow(["Post-Simuation Results:"])
        tally = {}
        for i, aft in enumerate(afters):
            lines, tally = aft.toCSV(i == 0, i == (len(afters)-1), tally)
            for l in lines:
                writer.writerow(l)
        writer.writerow([""])

        writer.writerow(["Recommendations:"])
        writer.writerow(["Region", "Party", "Defensive Seat"])
        for aft, party in zip(afters, rec_parties):
            row = [aft.name, party.name, "True" if party.at_risk else "False"]
            writer.writerow(row)

    if output:
        with open('data/recommend.json', 'w') as outfile:
            json.dump(data, outfile)
    print(json.dumps(data))

    return 0


def parseargs(args):
    parser = argparse.ArgumentParser(
            description="Generate recommendations for the 2019 EU elections in England, Wales and Scotland"
        )
    parser.add_argument("-r", "--region", type=str,
                        help="Generate recommentation for specific region")
    parser.add_argument("-u", "--update", action="store_true",
                        help="Update input files from GitHub")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show more detailed output")
    parser.add_argument("-o", "--output", action="store_true",
                        help="Output a recommendation file")
    parser.add_argument("-d", "--defence", action="store_true",
                        help="Use risk based analysis for defensive correction")
    parser.add_argument("-i", "--increment", type=int, default=10000,
                        help="vote increment for each iteration")

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs(sys.argv[1:])
    sys.exit(main(args))
