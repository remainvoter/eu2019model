import sys
import argparse

from .models import RecommendationEngine
from .utilities import DatabaseHelper


def main(args=None):
    """Console script for eu2019model."""

    db = DatabaseHelper(True)
    engine = RecommendationEngine()
    extra_turnout = 10
    for region in db.getAllRegions(extra_turnout):
        rec = engine.recommendRegion(region)
        if rec is not None:
            before, after, votes_taken, party = rec
            engine.print(before, after, party, votes_taken)

    return 0


def parseargs(args):
    parser = argparse.ArgumentParser(
            description="Generate recommendations for the 2019 EU elections in England, Wales and Scotland"
        )
    parser.add_argument("-r", "--region", type=str,
                        help="Generate recommentation for specific region")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show more detailed output")
    parser.add_argument("-t", "--turnout", type=int, default=0,
                        help="increase turnout in all regions in percentage")
    parser.add_argument("-i", "--increment", type=int, default=10000,
                        help="vote increment for each iteration")

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs(sys.argv[1:])
    sys.exit(main(args))
