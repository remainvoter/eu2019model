import sqlite3
from typing import List

from .eu2019model import Region, Party


class DatabaseHelper(object):

    def __init__(self):
        self.conn = sqlite3.connect('data/recommend_engine.db')
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

    def getRegionName(self, postcode: str) -> str:
        postcode = postcode.replace(' ', '').upper()
        q = f"SELECT eu_region FROM postcodes WHERE postcode = '{postcode}'"
        self.cur.execute(q)
        return self.cur.fetchall()[0][0]

    def getRegionFromPostcode(self, postcode: str) -> Region:
        name = self.getRegionName(postcode)
        return self.getRegion(name)

    def getRegion(self, name) -> Region:

        q = (f"SELECT * FROM regions WHERE eu_region = '{name}'")
        self.cur.execute(q)

        # Region info:
        name, seats, pop, turnout = self.cur.fetchall()[0]

        # Get a list of parties along with vote info
        parties = []
        q = f"SELECT party,percentage FROM projection WHERE region = '{name}'"
        self.cur.execute(q)
        for party, percentage in self.cur.fetchall():
            parties.append(Party(party, percentage*(pop*turnout/100)))

        return Region(name, parties, seats)

    def getAllRegions(self) -> List[Region]:

        q = "SELECT eu_region FROM regions"
        self.cur.execute(q)

        regions = []

        for name, in self.cur.fetchall():
            print(name)
            if name == 'Northern Ireland':
                continue
            regions.append(self.getRegion(name))

        return regions
