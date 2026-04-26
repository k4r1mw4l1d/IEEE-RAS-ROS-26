class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class Members:
    def __init__(self):
        self.memberslist = []

    def add_player(self, playerobj):
        self.memberslist.append(playerobj)


p1 = Player("Karim")
p2 = Player("Mahmoud")
p3 = Player("Khairy")

members = Members()
members.add_player(p1)
members.add_player(p2)
members.add_player(p3)

for p in members.memberslist:
    print(p.name)