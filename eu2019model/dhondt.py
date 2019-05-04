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
        return (f"Party {self.name} | "
                f"Score: {self.score:0.0f} | "
                f"Seats: {self.seats}")


class Dhondt(object):

    def __init__(self, nSeats: int):
        self.numOfSeats: int = nSeats
        self.parties: List[Party] = []

    def addParty(self, party: Party):
        self.parties.append(party)

    def numberOfParties(self) -> int:
        return len(self.parties)

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
            print(f"Round {s+1}: Party {winner.name} wins!")

            for party in self.parties:
                party.updateScore()
                print(party)
            print("------")
            print("")
