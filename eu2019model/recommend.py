import sys
import argparse
import json

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
    engine = RecommendationEngine(increment, update)
    for region in engine.getAllRegions():
        rec = engine.recommendRegion(region, risk)
        if rec is not None:
            before, after, votes_taken, party = rec
            data.append(engine.toDict(before, after, party, votes_taken))
            # engine.print(before, after, party, votes_taken)

    # # Create csv file from data:
    # for region in engine.getAllRegions():
    #     for party in engine.getAllParties():

    if output:
        with open('data/recommend.json', 'w') as outfile:
            json.dump(data, outfile)
    print(json.dumps(data, indent=2))

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
