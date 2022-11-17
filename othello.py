# For this Othello class, the player only plays with the AI, and always have the black pieces (going first)

import random
import time
from IPython.display import clear_output

class othelloBoard():
    board = [ [" "]*8 for i in range(8)]
    pieces = {"black": [], "white": []}
    turn = "player"
    ending = False

    def __init__(self):
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

        self.pieces["black"].append((3,3))
        self.pieces["black"].append((4,4))
        self.pieces["white"].append((3,4))
        self.pieces["white"].append((4,3))

    def printBoard(self):
        HLINE = '  +---+---+---+---+---+---+---+---+'
        print('    0   1   2   3   4   5   6   7')
        print(HLINE)

        for y in range(8):
            print(y, end=' ')
            for x in range(8):
                print('| %s' % (self.board[x][y]), end=' ')
            print('|')
            print(HLINE)

    def inRange(self, tile):
        if tile[0]>=0 and tile[0]<=7 and tile[1]>=0 and tile[1]<=7:
            return True
        else:
            return False

    def isEmptyTile(self, tile):
        return tile not in self.pieces["black"] and tile not in self.pieces["white"]

    def getAdjacent(self, tile):
        left = (tile[0]-1, tile[1])
        right = (tile[0]+1, tile[1])
        up = (tile[0], tile[1]-1)
        down = (tile[0], tile[1]+1)
        upleft = (tile[0]-1, tile[1]-1)
        upright = (tile[0]+1, tile[1]-1)
        downleft = (tile[0]-1, tile[1]+1)
        downright = (tile[0]+1, tile[1]+1) 

        return (left, right, up, down, upleft, upright, downleft, downright)

    # Find empty adjacent tiles
    def getEmptyAdjacent(self, tile):
    
        directions = self.getAdjacent(tile)
        validAdjacents = list(filter(self.inRange, directions))
        emptyAdjacents = list(filter(self.isEmptyTile, validAdjacents))

        return emptyAdjacents

    def getLegalMoves(self, color):
        opponent = ""
        if color == "black":
            opponent = "white"
        elif color == "white":
            opponent = "black"

        legalMoves = []
        for tile in self.pieces[opponent]:
            legalMoves.extend(self.getAdjacent(tile))
        
        legalMoves = list(filter(self.inRange, legalMoves))
        legalMoves = list(filter(self.isEmptyTile, legalMoves))



        ### TODO: having a same color piece in the line
        
        return list(set(legalMoves))



    # Move generator
    def move(self):

        legalMovesBlack = self.getLegalMoves("black")
        legalMovesWhite = self.getLegalMoves("white")

        if self.turn == "player":
            
            print("Legal Moves Player:" + str(legalMovesBlack))
            
            inputMove = input()
            x,y = inputMove.split(",")
            nextMove = (int(x),int(y))

            while nextMove not in legalMovesBlack:
                print("Illegal move, please retry")
                inputMove = input()
                x,y = inputMove.split(" ")
                nextMove = (int(x),int(y))

            print("Move: " + str(nextMove))
            
            self.board[int(x)][int(y)] = 2
            self.pieces["black"].append(nextMove)
            self.turn = "AI"
            
        elif self.turn == "AI":
            
            print("Legal Moves AI:" + str(legalMovesBlack))
            nextMove = random.choice(legalMovesWhite)

            self.board[nextMove[0]][nextMove[1]] = 1
            self.pieces["white"].append(nextMove)
            print("AI Move: " + str(nextMove))
            self.turn = "player"
        
        self.printBoard()

    def play(self):
        self.printBoard()
        while self.ending == False:
            self.move()


newGame = othelloBoard()
newGame.play()
