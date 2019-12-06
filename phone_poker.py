from primes import Prime
import random

class Player:
    counter = 0
    p = 0
    
    def __init__(self):
        self.__gen_key()
        self.hand = []
        Player.counter += 1
        self.id = Player.counter
        
    def __str__(self):
        return "Player " + str(self.id)
        
    def __gen_key(self):
        if Player.p != 0:
            self.__c = Prime.mutprime(Player.p - 1)
            self.__d = Prime.invert(self.__c, Player.p - 1)

    def encrypt(self, x):
        if Player.p != 0:
            return pow(x, self.__c, Player.p)
        return 0
    
    def decrypt(self, y):
        if Player.p != 0:
            return pow(y, self.__d, Player.p)
        return 0
    
    def take(self, deck, players):
        if len(deck) > 0 and len(players) > 0:
            i = random.randint(0, len(deck) - 1)
            rcard = deck.pop(i)
            for player in players:
                if player != self:
                    rcard = player.decrypt(rcard)
            self.hand += [self.decrypt(rcard)]
        
def encrypt_deck(deck, players):
    if len(players) > 0 and len(deck) >= len(players):
        for player in players:
            for card in range(len(deck)):
                deck[card] = player.encrypt(deck[card])
            random.shuffle(deck)

def deal(deck, players):
    if len(players) > 0:
        remains = len(deck) % len(players)
        while len(deck) > remains:
            for player in players:
                player.take(deck, players)
            

Player.p = 67

p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()

players = [p1, p2, p3, p4]
deck = [4, 5,+ 44, 21, 9, 30, 12, 31, 13, 60, 61, 62, 14, 2, 7]
print("Колода:\n" + str(deck))

encrypt_deck(deck, players)
print("Шифрованная колода:\n" + str(deck))

# Раздача
deal(deck, players)

for player in players:
    print(str(player) + ": " + str(player.hand))
print("Зашифрованный остаток колоды: " + str(deck))
