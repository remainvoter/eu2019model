# -*- coding: utf-8 -*-

"""Console script for eu2019model."""
import sys
import click

# from .dhondt import Dhondt, Party
from .utilities import DatabaseHelper
from .eu2019model import RecommendationEngine


@click.command()
def main(args=None):
    """Console script for eu2019model."""

    db = DatabaseHelper()
    engine = RecommendationEngine()

    recs = dict()
    for region in db.getAllRegions():

        print(f"Simulating for {region.name}...")
        rec = engine.recommendRegion(region)

        recs[region] = rec

        if rec is not None:
            before, region, votes_to_add, party = rec
            print(f"Recommendation for {region.name} is {party.name}")

    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
