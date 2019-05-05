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
        engine.recommendRegion(region)

    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
