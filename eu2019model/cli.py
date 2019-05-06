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
    for region in db.getAllRegions():
        rec = engine.recommendRegion(region)
        if rec is not None:
            before, after, votes_taken, party = rec
            engine.print(before, after, party, votes_taken)

    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
