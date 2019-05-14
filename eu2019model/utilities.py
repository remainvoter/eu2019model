import sqlite3
from typing import List
import os
import requests

from .eu2019model import Region, Party, VoteIntention
from .constants import recommended_parties, main_parties


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


class DatabaseHelper(object):

    def __init__(self):

        db_file = 'data/recommend_engine.db'
        if not os.path.isfile(db_file):
            id = '1QVnMwm3934wQFkZZf7r-tAPds-kKhFdo'
            download_file_from_google_drive(id, db_file)

        self.conn = sqlite3.connect(db_file)
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

    def getRegion(self, name, turnout_mod: int = 0) -> Region:

        q = (f"SELECT * FROM regions WHERE eu_region = '{name}'")
        self.cur.execute(q)

        # Region info:
        name, seats, pop, turnout = self.cur.fetchall()[0]
        turnout += turnout_mod

        # Get a list of parties along with vote info
        parties = []
        q = f"SELECT party,percentage FROM projection WHERE region = '{name}'"
        self.cur.execute(q)
        for party, percentage in self.cur.fetchall():
            party_name = party
            if party_name == 'SNP/Plaid Cymru':
                if name == 'Scotland':
                    party_name = 'SNP'
                elif name == 'Wales':
                    party_name = 'Plaid Cymru'

            pro_eu = party_name in recommended_parties
            main = party_name in main_parties

            parties.append(Party(
                party, percentage*(pop*turnout/100)/100,
                pro_eu, main))

        return Region(name, parties, seats, pop, turnout)

    def getIntendedVotes(self, intended_party: Party) -> List[VoteIntention]:

        party_name = intended_party.name
        if party_name in ['SNP', 'Plaid Cymru']:
            party_name = 'SNP/Plaid Cymru'

        q = (f"SELECT voted_party,percentage FROM intention "
             f"WHERE intended_party = '{party_name}'")

        self.cur.execute(q)

        intentions = []
        for voted_party, percentage in self.cur.fetchall():
            intentions.append(VoteIntention(
                voted_party,
                intended_party.name,
                percentage))

        return intentions

    def getAllRegions(self, turnout_mod: int = 0) -> List[Region]:

        q = "SELECT eu_region FROM regions"
        self.cur.execute(q)

        regions = []

        for name, in self.cur.fetchall():
            if name == 'Northern Ireland':
                continue
            regions.append(self.getRegion(name, turnout_mod))

        return regions
