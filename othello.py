# For this Othello class, the player plays with the AI using the black pieces (going first)

import random
import time
from IPython.display import clear_output
import copy

class othelloBoard():
    board = [[" "]*8 for i in range(8)]
    turn = "player"
    ending = False

    def __init__(self):
        self.board[3][3] = "B"
        self.board[3][4] = "W"
        self.board[4][3] = "W"
        self.board[4][4] = "B"

    def getScore(self, board):
        blackScore = sum(x.count("B") for x in board)
        whiteScore = sum(x.count("W") for x in board)
        return (blackScore, whiteScore)

    # Q2: Evaluation function
    # Basic evaluation function
    def evalFunction(self, board):
        (blackScore, whiteScore) = self.getScore(board)
        return blackScore - whiteScore
        
    # Q4: Improved evaluation function
    def improvedEvalFunction(self, board):
        (blackScore, whiteScore) = self.getScore(board)
        currScore = whiteScore - blackScore
        corners = ((0,0),(0,7),(7,0),(7,7))
        for corner in corners:
            if (board[corner[0]][corner[1]] == "W"):
                currScore += 10
            elif (board[corner[0]][corner[1]] == "B"):
                currScore -= 10
        return currScore

    # Q5: Basic GUI, user can input next move through terminal
    def printBoard(self):
        clear_output(wait=True)
        HLINE = '  +---+---+---+---+---+---+---+---+'
        print('    0   1   2   3   4   5   6   7')
        print(HLINE)

        for y in range(8):
            print(y, end=' ')
            for x in range(8):
                print('| %s' % (self.board[x][y]), end=' ')
            print('|')
            print(HLINE)

        print()
        print("Score:")
        (blackScore, whiteScore) = self.getScore(self.board)
        print("Player (black): " + str(blackScore))
        print("AI (white): " + str(whiteScore))


    def inRange(self, tile):
        if tile[0]>=0 and tile[0]<=7 and tile[1]>=0 and tile[1]<=7:
            return True
        else:
            return False

    def getAdjacent(self, tile):
        left = (tile[0]-1, tile[1])
        right = (tile[0]+1, tile[1])
        up = (tile[0], tile[1]-1)
        down = (tile[0], tile[1]+1)
        upleft = (tile[0]-1, tile[1]-1)
        upright = (tile[0]+1, tile[1]-1)
        downleft = (tile[0]-1, tile[1]+1)
        downright = (tile[0]+1, tile[1]+1) 

        adjacent = (left, right, up, down, upleft, upright, downleft, downright)
        validAdjacents = list(filter(self.inRange, adjacent))

        return validAdjacents

    def getLegalMoves(self, board, player):
        tempBoard = copy.deepcopy(board)

        opponent = ""
        if player == "B":
            opponent = "W"
        elif player == "W":
            opponent = "B"

        emptyTiles = []
        legalMoves = []

        for i in range(8):
            for j in range(8):
                if tempBoard[i][j] == opponent:
                    emptyTiles.extend(self.getAdjacent((i,j)))
        
        emptyTiles = list(filter(self.inRange, emptyTiles))
        emptyTiles = list(filter(lambda x: (tempBoard[x[0]][x[1]] == " "), emptyTiles))


        for tile in emptyTiles:
            isLegal = False
            adjacent = self.getAdjacent(tile)
            oppAdjacent = list(filter(lambda x: (tempBoard[x[0]][x[1]] == opponent), adjacent))

            for oppTile in oppAdjacent:
                
                direction = (oppTile[0]-tile[0], oppTile[1]-tile[1])
                nextTileInDirection = (oppTile[0]+direction[0], oppTile[1]+direction[1])
                nextX = oppTile[0]+direction[0]
                nextY = oppTile[1]+direction[1]

                while True:           
                    # out of range
                    if (not self.inRange(nextTileInDirection)):
                        break
                    # player's color tile, the move is legal
                    elif (tempBoard[nextX][nextY] == player):
                        isLegal = True
                        break
                    # empty tile
                    elif (tempBoard[nextX][nextY] == " "):
                        break
                    # opponent's color tile, continue to next one
                    else:
                        nextTileInDirection = (nextTileInDirection[0]+direction[0], nextTileInDirection[1]+direction[1])
                        nextX = nextTileInDirection[0]
                        nextY = nextTileInDirection[1]         

            if isLegal:
                legalMoves.append(tile)

        return list(set(legalMoves))

    def flip(self, board, tile, player):
        tempBoard = copy.deepcopy(board)

        tempBoard[tile[0]][tile[1]] = player

        opponent = ""
        if player == "B":
            opponent = "W"
        elif player == "W":
            opponent = "B"

        adjacent = self.getAdjacent(tile)
        oppAdjacent = list(filter(lambda x: (tempBoard[x[0]][x[1]] == opponent), adjacent))

        for oppTile in oppAdjacent:
            direction = (oppTile[0]-tile[0], oppTile[1]-tile[1])
            nextX = oppTile[0]+direction[0]
            nextY = oppTile[1]+direction[1]
            nextTileInDirection = (oppTile[0]+direction[0], oppTile[1]+direction[1])
            route = [oppTile]

            while True:           
                # out of range
                if (not self.inRange(nextTileInDirection)):
                    route.clear()
                    break
                # player's color tile, the move is legal
                elif (tempBoard[nextX][nextY] == player):
                    break
                # empty tile
                elif (tempBoard[nextX][nextY] == " "):
                    route.clear()
                    break
                # opponent's color tile, continue to next one
                else:
                    route.append(nextTileInDirection)
                    nextTileInDirection = (nextTileInDirection[0]+direction[0], nextTileInDirection[1]+direction[1])      
                    nextX = nextTileInDirection[0]
                    nextY = nextTileInDirection[1] 

            for tileToFlip in route:
                if player == "B":
                    tempBoard[tileToFlip[0]][tileToFlip[1]] = "B"
                elif player == "W":
                    tempBoard[tileToFlip[0]][tileToFlip[1]] = "W"
        
        return tempBoard


    # Q2: Move generator
    def move(self):
        tempBoard = copy.deepcopy(self.board)

        legalMovesBlack = self.getLegalMoves(tempBoard, "B")
        legalMovesWhite = self.getLegalMoves(tempBoard, "W")

        if len(legalMovesBlack) and len(legalMovesWhite) == 0:
            self.ending = True
            return 
        elif len(legalMovesWhite) == 0:
            self.turn = "player"
        elif len(legalMovesBlack) == 0:
            self.turn = "AI"

        if self.turn == "player":
            
            print("Legal Moves Player:" + str(legalMovesBlack))
            inputMove = input()
            x,y = inputMove.split(",")
            nextMove = (int(x),int(y))

            while nextMove not in legalMovesBlack:
                print("Illegal move, please retry")
                inputMove = input()
                x,y = inputMove.split(",")
                nextMove = (int(x),int(y))
            
            newBoard = self.flip(tempBoard, nextMove, "B")
            self.board = newBoard
            self.turn = "AI"
            
        elif self.turn == "AI":
            
            if (len(legalMovesWhite) == 1):
                nextMove = legalMovesWhite[0]
            else:
                nextMove = self.alphaBeta(tempBoard, "", 3, float("-inf"), float("inf"), True)[1]
            newBoard = self.flip(tempBoard, nextMove, "W")
            self.board = newBoard
            self.turn = "player"


    # Q3: Alpha beta pruning for minimax algorithm
    def alphaBeta(self, board, move, depth, alpha, beta, maximizingPlayer):
        tempBoard = copy.deepcopy(board)

        legalMovesBlack = self.getLegalMoves(tempBoard, "B")
        legalMovesWhite = self.getLegalMoves(tempBoard, "W")
        gameOver = len(legalMovesBlack) == 0 and legalMovesWhite == 0
        if depth == 0 or gameOver:
            return (self.improvedEvalFunction(tempBoard), move)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            bestMove = legalMovesWhite[0]
            for moveChoice in legalMovesWhite:
                newBoard = self.flip(tempBoard, moveChoice, "W")
                eval = self.alphaBeta(newBoard, moveChoice, depth-1, alpha, beta, False)[0]
                if eval >= maxEval:
                    bestMove = moveChoice
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (maxEval, bestMove)

        else:
            minEval = float('inf')
            bestMove = legalMovesWhite[0]
            for moveChoice in legalMovesBlack:
                newBoard = self.flip(tempBoard, moveChoice, "B")
                eval = self.alphaBeta(newBoard, moveChoice, depth-1, alpha, beta, True)[0]
                if eval <= minEval:
                    bestMove = moveChoice
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (minEval, bestMove)


    def play(self):
        self.printBoard()
        while self.ending == False:
            self.move()
            self.printBoard()
            time.sleep(3)
        print("Game ended!")

newGame = othelloBoard()
newGame.play()
