# -*- coding: utf-8 -*-
from typing import List


class Party(object):

    def __init__(self, name: str, votes: int):
        self.name: str = name
        self.votes: int = votes
        self.seats: int = 0
        self.score: float = float(votes)

    def addSeat(self):
        self.seats += 1

    def reset(self):
        self.seats = 0

    def addVotes(self, additionalVotes: int):
        self.votes += additionalVotes

    def updateScore(self):
        self.score = self.votes/(self.seats+1)

    def __str__(self):
        return (f"{self.name:<16} | "
                f"Score: {self.score:9.0f} | "
                f"Seats: {self.seats}")


class Region(object):

    def __init__(self, name: str, parties: List[Party], numOfSeats: int):
        from .dhondt import Dhondt
        self.dh = Dhondt(numOfSeats)
        self.dh.addParties(parties)
        self.name = name


class Projection(object):

    def __init__(self, party: Party, region: Region):
        pass


class RecommendationEngine(object):

    def __init__(self, voteIncrement: int = 10000):
        self.voteIncrement = voteIncrement

    def recommendRegion(self, region: Region):
        """Do this for each region..."""

        print(f"Initial simulation for {region.name}")
        region.dh.simulate()
        print("-------")
# for (increment n_thousand_votes):
#     for recommendation in {SNP, LibDem, CUK, Green}:
#         remove n_thousand_votes proportionally
#         add n_thousand_votes to recommendation
#         dhondt_after = calculate_dhondt
#         if (dhondt_after > dhondt_before)
#             return {dh_before, recommendation, n_thousand_votes, dh_after}
#         else
#             reset dhondt_after
