import random
class Game(): # main game class
    def __init__(self, num_players) -> None:
        self.players = [Player() for i in range(num_players)]
        self.board = Board()

    def logic(self): # main logic function
        done = False
        round = 1
        while not done: 
            print(); print(); print("Round", round); print(); round+=1
            i = 1
            while i < len(self.players) and not done: # for every player, we move them one after the other, then we output what they rolled, where they landed, if they hit snakes, ladders or none, and if they won
                print(); print("Player", i+1, "turn. They're at", self.players[i].get_pos())
                self.players[i].roll()
                self.players[i].set_pos(self.board.move_player(self.players[i].get_pos()))
                print("Player", i+1, "moves to", self.players[i].get_pos())
                if self.players[i].get_pos() == 100:
                    done = True
                    print("Congratulations, Player", i+1, "Won")

class Player(): 
    def __init__(self) -> None:
        self.pos = 0
    
    def roll(self): # rolling the dice
        roll = random.randint(1,6); print("The dice rolled", roll)
        self.pos += roll
        if self.pos > 100:
            self.pos = 200 - self.pos

    def set_pos(self, x): 
        self.pos = x

    def get_pos(self):
        return self.pos

class Board(): # this is the class of the board
    def __init__(self) -> None:
        self.snakes =  {}
        self.ladders = {}
        for i in range(1,11):
            n = random.randint(1,10)
            n1 = random.randint(1,10)
            while n == n1:
                n1 = random.randint(1,10)
            

    def move_player(self, pos): # moving the player on the board, including snakes and ladders
        if pos in self.snakes:
            pos = self.snakes[pos]
            print("HAHA Player Landed on a snake")
        elif pos in self.ladders:
            pos = self.ladders[pos]
            print("WOW Player is on a ladder")
        return pos
g = Game(2)
g.logic()