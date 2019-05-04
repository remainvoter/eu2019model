import sqlite3
import csv
from typing import List

from .constants import Constants
from .eu2019model import Region, Projection


class PostCode(object):

    def __init__(self, postcode: str):
        self.postcode = postcode.replace(' ', '').upper()
        self.conn = sqlite3.connect(Constants().postcodes)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

    def getRegion(self) -> Region:
        q = (f"SELECT * FROM regions WHERE eu_region = (SELECT eu_region "
             f"FROM postcodes WHERE postcode = '{self.postcode}')")
        self.cur.execute(q)

        name, seats, pop, turnout = self.cur.fetchall()[0]


def loadProjections() -> List[Projection]:

    url = Constants().projected2019
    with open(url) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            line_count += 1