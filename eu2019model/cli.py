# -*- coding: utf-8 -*-

"""Console script for eu2019model."""
import sys
import click

# from .dhondt import Dhondt, Party
from .utilities import DatabaseHelper


@click.command()
def main(args=None):
    """Console script for eu2019model."""

    db = DatabaseHelper()
    r = db.getRegion('NE29 6Ta')

    print(r)

    # # Create a vote:
    # dh = Dhondt(8)

    # # Create some parties:
    # dh.addParty(Party('C', 30000))
    # dh.addParty(Party('B', 80000))
    # dh.addParty(Party('A', 100000))
    # dh.addParty(Party('D', 20000))

    # # Simulate!
    # dh.simulate()

    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
