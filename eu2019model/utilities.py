import sqlite3
from typing import List
import os
import requests
import csv

from .models import Region, Party, VoteIntention
from .constants import recommended_parties, main_parties


class DatabaseHelper(object):

    def __init__(self, recreate: bool = False):

        self.recreate = recreate

        if recreate:
            self.db_file = 'https://dbhub.io/DrNickMartin/recommend_engine.db'
        else:
            self.db_file = 'data/recommend_engine.db'
        
        self.pathA = 'data/A.csv'
        self.pathB = 'data/B.csv'
        self.pathC = 'data/C.csv'
        self.pathD = 'data/D'

        self.getConnection()

        if self.recreate:
            self.downloadInputs()
            self.createDatabase()
            self.loadIntentions()
            self.loadProjections()

    def getRegionName(self, postcode: str) -> str:
        postcode = postcode.replace(' ', '').upper()
        q = f"SELECT eu_region FROM postcodes WHERE postcode = '{postcode}'"
        self.cur.execute(q)
        return self.cur.fetchall()[0][0]

    def getRegion(self, name, turnout_mod: int = 0) -> Region:

        q = (f"SELECT * FROM regions WHERE eu_region = '{name}'")
        self.cur.execute(q)

        # Region info:
        name, seats, pop, turnout = self.cur.fetchall()[0]
        turnout += turnout_mod

        # Get a list of parties along with vote info
        parties = []
        q = f"SELECT party,percentage FROM projection WHERE lower(region) = '{name.lower()}'"
        self.cur.execute(q)
        for party, percentage in self.cur.fetchall():
            party_name = party
            pro_eu = party_name in recommended_parties
            main = party_name in main_parties

            parties.append(Party(
                party, percentage*(pop*turnout/100)/100,
                pro_eu, main))

        return Region(name, parties, seats, pop, turnout)

    def getIntendedVotes(self, redist_part: Party, region: Region) -> List[VoteIntention]:

        q = (f"SELECT swing_from,percent FROM intention "
             f"WHERE swing_to = '{redist_part.name}'"
             f"AND region = '{region.name}'")

        self.cur.execute(q)

        intentions = []
        for swingFrom, percent in self.cur.fetchall():
            intentions.append(VoteIntention(
                swingFrom,
                redist_part.name,
                percent))

        return intentions

    def getAllRegions(self) -> List[Region]:

        with open(self.pathD) as f:
            turnout_mod = int(f.read())

        q = "SELECT eu_region FROM regions"
        self.cur.execute(q)

        regions = []

        for name, in self.cur.fetchall():
            regions.append(self.getRegion(name, turnout_mod))

        return regions

    def getConnection(self):

        if self.recreate and os.path.isfile(self.db_file):
            os.remove(self.db_file)

        conn = sqlite3.connect(self.db_file)
        conn.text_factory = str
        self.cur = conn.cursor()

    def downloadInputs(self):

        if os.path.isfile(self.pathA):
            os.remove(self.pathA)

        if os.path.isfile(self.pathB):
            os.remove(self.pathB)

        if os.path.isfile(self.pathC):
            os.remove(self.pathC)

        if os.path.isfile(self.pathD):
            os.remove(self.pathD)

        urlA = 'https://raw.githubusercontent.com/remainvoter/eu2019/master/input_data/A_expected_total_voters.csv'
        urlB = 'https://raw.githubusercontent.com/remainvoter/eu2019/master/input_data/B_EU_2019_intentions.csv'
        urlC = 'https://raw.githubusercontent.com/remainvoter/eu2019/master/input_data/C_voter_swings.csv'
        urlD = 'https://raw.githubusercontent.com/remainvoter/eu2019/master/input_data/D_increased_turnout_percentage'

        tokenA = 'AD4HAFLEN3FLZWBTTAEGMQ24433AO'
        tokenB = 'AD4HAFNDJCMIAM4PFST6GJK4434YW'
        tokenC = 'AD4HAFKRIN53DM3UANNX3G24434Z6'
        tokenD = 'AL7PP3PYUFDUJWKPBCO2IZC45GQAQ'

        rA = requests.get(f'{urlA}?token={tokenA}', allow_redirects=True)
        rB = requests.get(f'{urlB}?token={tokenB}', allow_redirects=True)
        rC = requests.get(f'{urlC}?token={tokenC}', allow_redirects=True)
        rD = requests.get(f'{urlD}?token={tokenD}', allow_redirects=True)

        open('data/A.csv', 'wb').write(rA.content)
        open('data/B.csv', 'wb').write(rB.content)
        open('data/C.csv', 'wb').write(rC.content)
        open('data/D', 'wb').write(rD.content)

    def createDatabase(self):
        with open("data/recommend_schema.sql") as f:
            self.cur.executescript(' '.join(f.readlines()))

    def loadIntentions(self):

        with open(self.pathC) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            sql_base = ("INSERT INTO 'intention'('region',"
                        "'swing_to','swing_from','percent') VALUES")
            values = []
            for line, row in enumerate(csv_reader):
                if line > 0:
                    values.append((f"('{row[0].replace('_',' ')}',"
                                   f"'{row[1].replace('_',' ')}',"
                                   f"'{row[2].replace('_',' ')}',"
                                   f"'{int(row[3])}')"))

            self.cur.execute("BEGIN TRANSACTION")
            q = f"{sql_base} {','.join(values)}"
            self.cur.execute(q)
            self.cur.execute("COMMIT")

    def loadProjections(self):

        parties = []
        region_names = []
        percentages = dict()
        with open(self.pathB) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                for i, item in enumerate(row):
                    if line_count == 0:
                        if i > 0:
                            region_name = item.replace('_', ' ').lstrip()
                            percentages[region_name] = []
                            region_names.append(region_name)
                    else:
                        if i == 0:
                            parties.append(item.replace('_', ' '))
                        else:
                            percentages[region_names[i-1]].append(float(item))

                line_count += 1

        sql_base = ("INSERT INTO 'projection'('party',"
                    "'region','percentage') VALUES")
        values = []
        for region in percentages:
            for pind, percent in enumerate(percentages[region]):
                values.append((f"('{parties[pind]}',"
                               f"'{region}',"
                               f"'{percent}')"))
        self.cur.execute("BEGIN TRANSACTION")
        q = f"{sql_base} {','.join(values)}"
        self.cur.execute(q)
        self.cur.execute("COMMIT")
