from typing import List

from .models import Party


class Dhondt(object):

    def __init__(self, nSeats: int, verbose: bool = False):
        self.numOfSeats: int = nSeats
        self.parties: List[Party] = []
        self.verbose = verbose

    def addParty(self, party: Party):
        self.parties.append(party)

    def numberOfParties(self) -> int:
        return len(self.parties)

    def addParties(self, parties: List[Party]):
        self.parties.extend(parties)

    def toDict(self):

        self.parties.sort(key=lambda p: p.order)

        data = {}
        for p in self.parties:
            if p.seats == 0:
                continue

            data[p.name] = p.seats

        return data

    def simulate(self):

        # Check we have some parties
        if self.numberOfParties() == 0:
            raise Exception("There aren't any parties to simulate...")
            return

        # Check the party names are unique...
        if self.numberOfParties() > len(set(p.name for p in self.parties)):
            raise Exception("Party names must be unique")
            return

        for s in range(self.numOfSeats):
            self.parties.sort(key=lambda p: p.score, reverse=True)

            scores = [p.score for p in self.parties]

            if self.numberOfParties() == len(set(scores)):
                winner = self.parties[0]
            elif self.parties[0].score in scores[1:]:
                for i, party in enumerate(self.parties):
                    if party.score != self.parties[0].score:
                        winner = self.parties[i-1]
                        break
            else:
                winner = self.parties[0]

            winner.addSeat()

            if winner.order == 100:
                winner.order = s

            if self.verbose:
                print(f"Round {s+1}: {winner.name} wins!")

            for party in self.parties:
                party.updateScore()
                if self.verbose:
                    print(party)

            if self.verbose:
                print("------")
                print("")
