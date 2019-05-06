# -*- coding: utf-8 -*-
from typing import List, Tuple
import copy
import math


class Party(object):

    def __init__(self, name: str, votes: int, proEU: bool,
                 main: bool, seats: int = 0):
        self.name: str = name
        self.votes: int = votes
        self.seats: int = seats
        self.score: float = float(votes)
        self.proEU: bool = proEU
        self.main: bool = main

    def copy(self):
        return Party(
            str(self.name),
            int(self.votes),
            bool(self.proEU),
            bool(self.main),
            int(self.seats))

    def addSeat(self):
        self.seats += 1

    def reset(self):
        self.seats = 0
        self.score = float(self.votes)

    def addVotes(self, additionalVotes: int):
        self.votes += additionalVotes

    def updateScore(self):
        self.score = self.votes/(self.seats+1)

    def __str__(self):
        return (f"{self.name:<16} | "
                f"Votes: {self.votes:9.0f} | "
                f"Seats: {self.seats}")

    def isSNPorPlaid(self):
        return self.name in ['Plaid Cymru', 'SNP']

    def equal(self, party_name: str):
        if self.isSNPorPlaid() and party_name == 'SNP/Plaid Cymru':
            return True
        else:
            return party_name == self.name


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

    def reset(self):
        for p in self.dh.parties:
            p.reset()

    def compare(self, other):
        for p in self.dh.parties:
            ind = other.getPartyIndex(p.name)
            pother = other.dh.parties[ind]
            print((f"{p.name:<17} vote diff: "
                   f"{math.floor(pother.votes-p.votes):0.0f}"))

    def redistributeVotes(self, voteIncrement: int, redist_party: Party):
        from .utilities import DatabaseHelper
        dbh = DatabaseHelper()

        votes_taken = 0
        # votes_to_take = self.population*(self.turnout/100)
        votes_to_take = voteIncrement
        intentions = dbh.getIntendedVotes(redist_party)

        # Loop over the three main parties and
        # remove propotionately
        other_percentates = 0
        perc_check = []
        for party in self.dh.parties:

            if party.equal(redist_party.name):
                continue

            # Get the intended swing percentage
            for intent in intentions:
                if party.equal(intent.intended):
                    break

            if not party.main:
                other_percentates += intent.percentage/100
                perc_check.append(intent.percentage/100)
                continue

            votesToRemove = votes_to_take*(intent.percentage/100)
            party_index = self.getPartyIndex(intent.intended)
            currentVotes = self.dh.parties[party_index].votes

            # Check if we have some votes to remove
            if currentVotes == 0:
                continue

            # Make sure we don't go negative...
            if (currentVotes - votesToRemove) < 0:
                votesToRemove = votesToRemove

            # Remove the votes
            self.dh.parties[party_index].votes -= votesToRemove

            # Keep track of how many votes have been removed
            votes_taken += votesToRemove

        if self.dh.verbose:
            print(f"Removed {votes_taken} from main parties")

        votes_from_others = votes_to_take - votes_taken

        if self.dh.verbose:
            print(f"Still need to remove {votes_from_others} votes")

        percent_check = 0
        for party in self.dh.parties:

            if party.main or party.equal(redist_party.name):
                continue

            # Get the intended swing percentage
            for intent in intentions:
                if party.equal(intent.intended):
                    break

            percent_to_remove = (intent.percentage/100)/other_percentates
            percent_check += percent_to_remove
            votesToRemove = votes_from_others*(percent_to_remove)
            party_index = self.getPartyIndex(intent.intended)
            currentVotes = self.dh.parties[party_index].votes

            # Check if we have some votes to remove
            if currentVotes == 0:
                continue

            # Make sure we don't go negative...
            if (currentVotes - votesToRemove) < 0:
                votesToRemove = votesToRemove

            # Remove the votes
            self.dh.parties[party_index].votes -= votesToRemove

            # Keep track of how many votes have been removed
            votes_taken += votesToRemove

        if self.dh.verbose:
            print(f"Removed {votes_from_others} from other parties")

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
                return i
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

    def __init__(self, intended_party: str, voted_party: str,
                 percentage: int):

        self.intended: str = intended_party
        self.voted: str = voted_party
        self.percentage: int = percentage


class RecommendationEngine(object):

    def __init__(self, voteIncrement: int = 10000):
        self.voteIncrement = voteIncrement

    def printParties(self, region: Region):
        party_list = [p.copy() for p in region.dh.parties]
        [print(p) for p in party_list]

    def print(self, before: Region, after: Region,
              rec_party: Party, votes: int):
        before_parties = before.dh.parties
        before_parties.sort(key=lambda p: p.name)

        after_parties = after.dh.parties
        after_parties.sort(key=lambda p: p.name)

        print_line = []

        print_line.append(f"{before.name}")
        print_line.append(''.join([str(p.seats) for p in before_parties]))
        print_line.append(f"{rec_party.name}")
        print_line.append(f"{math.floor(votes):0.0f}")
        print_line.append(''.join([str(p.seats) for p in after_parties]))

        print(','.join(print_line))

    def recommendRegion(self, region: Region, max_iters: int = 500):
        """Do this for each region..."""

        if region.isRemain():
            return None

        if region.dh.verbose:
            print(f"Initial simulation for {region.name}")
        region.simulate()
        before = region.copy()

        votes_to_add = 0
        for i in range(max_iters):  # Incrememnt loop
            votes_to_add += self.voteIncrement
            party_list = copy.deepcopy(region.dh.parties)
            for party in party_list:
                if not party.proEU:
                    continue

                self.printParties(region)
                votes_added = region.redistributeVotes(votes_to_add, party)

                print(f"Added {votes_added:0.0f} votes to {party.name}")

                if region.dh.verbose:
                    print(f"Resimulating:")
                region.reset()
                region.simulate()

                before.compare(region)
                self.print(before.copy(), region.copy(), party, votes_added)

                print("---")

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
