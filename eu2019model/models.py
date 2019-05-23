# -*- coding: utf-8 -*-
from typing import List, Tuple
import copy
import math


class Party(object):

    def __init__(self, name: str, votes: int, proEU: bool,
                 main: bool, order: int = 100, seats: int = 0,
                 affiliation: str = "", at_risk: bool = False):
        self.name: str = name
        self.votes: int = votes
        self.seats: int = seats
        self.score: int = votes
        self.proEU: bool = proEU
        self.main: bool = main
        self.order: int = order
        self.affiliation: str = affiliation
        self.at_risk: bool = at_risk

    def copy(self):
        return Party(
            str(self.name),
            int(self.votes),
            bool(self.proEU),
            bool(self.main),
            int(self.order),
            int(self.seats),
            str(self.affiliation),
            bool(self.at_risk))

    def addSeat(self):
        self.seats += 1

    def reset(self):
        self.seats = 0
        self.score = float(self.votes)

    def addVotes(self, additionalVotes: int):
        self.votes += additionalVotes

    def updateScore(self):
        self.score = int(math.floor(self.votes/(self.seats+1)))

    def __str__(self):
        return (f"{self.name:<17} | "
                f"Votes: {self.score:9.0f} | "
                f"Seats: {self.seats}")

    def isSNPorPlaid(self):
        return self.name in ['Plaid Cymru', 'SNP']

    def equal(self, party_name: str):
        return party_name.lower() == self.name.lower()


class Region(object):

    def __init__(self, name: str, parties: List[Party],
                 numOfSeats: int, population: int, turnout: float):
        from .dhondt import Dhondt
        self.dh = Dhondt(numOfSeats)
        self.dh.addParties(parties)
        self.name = name
        self.computed = False
        self.population = population
        self.turnout = turnout

    def copy(self):

        new_parties = []
        for p in self.dh.parties:
            new_parties.append(p.copy())

        return Region(
            str(self.name),
            new_parties,
            int(self.dh.numOfSeats),
            int(self.population),
            float(self.turnout))

    def toCSV(self, first_line: bool, last_line: bool, tally: dict):

        lines = []
        self.dh.parties.sort(key=lambda p: p.name)

        if first_line:
            row1 = ["Party:"]
            for party in self.dh.parties:
                if party.name not in tally.keys():
                    tally[party.name] = []
                row1.append(party.name)
            lines.append(row1)

        row = [self.name]
        for party in self.dh.parties:
            row.append(f"{party.seats}")
            tally[party.name].append(party.seats)
        lines.append(row)

        if last_line:
            rowm2 = ["Total"]
            rowm1 = [""]
            aff_tot = {}
            for party in self.dh.parties:
                rowm2.append(sum(tally[party.name]))
                if party.affiliation not in aff_tot.keys():
                    aff_tot[party.affiliation] = 0
                aff_tot[party.affiliation] += sum(tally[party.name])
            rowaf1 = ["Affiliation:"]
            rowaf2 = ["Total:"]
            for k, v in aff_tot.items():
                rowaf1.append(k)
                rowaf2.append(str(v))
            lines.append(rowm2)
            lines.append(rowm1)
            lines.append(rowaf1)
            lines.append(rowaf2)

        return lines, tally

    def isScotlandOrWales(self):
        return self.name in ['Scotland', 'Wales']

    def reset(self):
        for p in self.dh.parties:
            p.reset()

    def compare(self, other):
        for p in self.dh.parties:
            ind = other.getPartyIndex(p.name)
            pother = other.dh.parties[ind]
            print((f"{p.name:<17} vote diff: "
                   f"{math.floor(pother.votes-p.votes):0.0f}"))

    def redistributeVotes(self, voteIncrement: int, redist_party: Party, dbh):

        votes_taken = 0
        votes_to_take = voteIncrement
        intentions = dbh.getIntendedVotes(redist_party, self)

        for intent in intentions:

            rem_i = self.getPartyIndex(intent.swingFrom)

            if redist_party.equal(intent.swingFrom):
                continue

            if self.dh.parties[rem_i].main:
                votesToRemove = votes_to_take*(intent.percent/100)
                currentVotes = self.dh.parties[rem_i].votes

                # Check if we have some votes to remove
                if currentVotes == 0:
                    continue

                # Make sure we don't go negative...
                if (currentVotes - votesToRemove) < 0:
                    votesToRemove = votesToRemove

                # Remove the votes
                self.dh.parties[rem_i].votes -= votesToRemove

                # Keep track of how many votes have been removed
                votes_taken += votesToRemove

        if self.dh.verbose:
            print(f"Removed {votes_taken} from main parties")

        # Add those votes to the redistributing party
        redist_party_index = self.getPartyIndex(redist_party.name)
        self.dh.parties[redist_party_index].votes += votes_taken

        if self.dh.verbose:
            print(f"Added {votes_taken} to {redist_party.name}")

        return votes_taken

    def simulate(self):
        self.dh.simulate()
        self.computed = True

    def getPartyIndex(self, name):
        for i, p in enumerate(self.dh.parties):
            if p.equal(name):
                return int(i)
        raise Exception("Couldn't find party")

    def isRemain(self):
        return self.seatsToRemain() < 0

    def getSeatSplit(self) -> Tuple[int]:
        leave = 0
        remain = 0
        for p in self.dh.parties:
            if p.proEU:
                remain += p.seats
            else:
                leave += p.seats

        return leave, remain

    def getRemainSeats(self):
        return self.getSeatSplit()[1]

    def seatsToRemain(self):

        leave, remain = self.getSeatSplit()
        return leave - remain

    def moreRamainSeats(self, other):
        remain = self.getSeatSplit()[1]
        other_remain = other.getSeatSplit()[1]
        return remain > other_remain


class VoteIntention(object):

    def __init__(self, swingFrom: str, swingTo: str,
                 percent: int):

        self.swingFrom: str = swingFrom
        self.swingTo: str = swingTo
        self.percent: int = percent


class RecommendationEngine(object):

    def __init__(self, voteIncrement: int = 10000, update: bool = True):
        from .utilities import DatabaseHelper
        self.voteIncrement = voteIncrement
        self.dbh = DatabaseHelper(update)

    def printParties(self, region: Region):
        party_list = [p.copy() for p in region.dh.parties]
        [print(p) for p in party_list]

    def getAllRegions(self):
        return self.dbh.getAllRegions()

    def toDict(self, before: Region, after: Region,
               rec_party: Party, votes: int):

        data = {}

        data["recommendation"] = rec_party.name
        data["region"] = before.name
        data["swing-votes"] = votes
        data["pre-dhondt-seats"] = before.dh.toDict()
        data["post-dhondt-seats"] = after.dh.toDict()

        return data

    def print(self, before: Region, after: Region,
              rec_party: Party, votes: int):
        before_parties = before.dh.parties
        before_parties.sort(key=lambda p: p.order)

        after_parties = after.dh.parties
        after_parties.sort(key=lambda p: p.order)

        print_line = []

        print_line.append(f"{before.name}")
        print_line.append(''.join([str(p.seats) for p in before_parties]))
        print_line.append(f"{rec_party.name}")
        print_line.append(f"{math.floor(votes):0.0f}")
        print_line.append(''.join([str(p.seats) for p in after_parties]))

        print(','.join(print_line))

    def addRiskFactor(self, region: Region):
        from . import constants
        risk_check = region.copy()

        # Calculate risk factor
        # If there aren't any remain parties then risk factor is 0:
        have_remain = False
        for p in risk_check.dh.parties:
            if p.name in constants.recommended_parties and p.seats > 0:
                have_remain = True
                break

        if have_remain:
            # Find lowest remain seat:
            max_order = 0
            risk_party = None
            for p in risk_check.dh.parties:
                if p.name in constants.recommended_parties and p.seats > 0:
                    if p.order > max_order:
                        max_order = int(p.order)
                        risk_party = p.copy()

            if risk_party is None:
                return None

            # Calculate number of votes to loose seat
            curr_seats = int(risk_party.seats)
            inc = 100
            votes_removed = 0

            while risk_party.seats == curr_seats:
                # Remove votes from risk party and add to brexit party
                p_ind = risk_check.getPartyIndex(risk_party.name)
                bp_ind = risk_check.getPartyIndex('Brexit Party')
                risk_check.dh.parties[p_ind].votes -= inc
                risk_check.dh.parties[bp_ind].votes += inc

                risk_check.reset()
                risk_check.simulate()
                votes_removed += inc
                p_ind = risk_check.getPartyIndex(risk_party.name)
                risk_party = risk_check.dh.parties[p_ind].copy()
            risk = math.floor((1/votes_removed)*8000)/100
            print(f"{risk_check.name}, {risk_party.name}:, {votes_removed}")

            # Add risk% votes to the at risk party
            p_ind = region.getPartyIndex(risk_party.name)
            pop = region.population
            to = region.turnout/100
            add_votes = pop*to*risk
            if add_votes > 0:
                region.dh.parties[p_ind].votes += add_votes
                region.dh.parties[p_ind].at_risk = True
                return p_ind
            else:
                return None

        else:
            return None

    def recommendRegion(self, region: Region, risk: bool, max_iters: int = 5000):
        """Do this for each region..."""

        if region.dh.verbose:
            print(f"Initial simulation for {region.name}")

        region.simulate()
        before = region.copy()

        if risk:
            ind = self.addRiskFactor(region)
            if ind is not None:
                before.dh.parties[ind].at_risk = True

        votes_to_add = 0
        for i in range(max_iters):  # Incrememnt loop
            votes_to_add += self.voteIncrement
            party_list = copy.deepcopy(region.dh.parties)
            for party in party_list:
                if not party.proEU:
                    continue

                if party.isSNPorPlaid() and not region.isScotlandOrWales():
                    continue

                votes_added = region.redistributeVotes(votes_to_add, party, self.dbh)

                if region.dh.verbose:
                    print(f"Resimulating:")
                region.reset()
                region.simulate()

                # Should we recommend?
                if region.moreRamainSeats(before):
                    return (
                        before.copy(),
                        region.copy(),
                        votes_added,
                        party.copy())
                else:
                    region = before.copy()

        return None
