import sys
import argparse
import json

from .models import RecommendationEngine


def main(args=None):
    """Console script for eu2019model."""

    if args is None:
        update = True
        increment = 10000
        output = False
    else:
        update = args.update
        increment = args.increment
        output = args.output

    data = []
    engine = RecommendationEngine(increment, update)
    for region in engine.getAllRegions():
        rec = engine.recommendRegion(region)
        if rec is not None:
            before, after, votes_taken, party = rec
            data.append(engine.toDict(before, after, party, votes_taken))

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
    parser.add_argument("-i", "--increment", type=int, default=10000,
                        help="vote increment for each iteration")

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs(sys.argv[1:])
    sys.exit(main(args))
