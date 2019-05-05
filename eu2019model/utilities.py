import sqlite3
from .eu2019model import Region, Party


class DatabaseHelper(object):

    def __init__(self):
        self.conn = sqlite3.connect('data/recommend_engine.db')
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

    def getRegion(self, postcode: str) -> Region:
        postcode = postcode.replace(' ', '').upper()
        q = (f"SELECT * FROM regions WHERE eu_region = (SELECT eu_region "
             f"FROM postcodes WHERE postcode = '{postcode}')")
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