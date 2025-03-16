class GameState():
    def __init__(self):
        #board: 8x8 2d list, moi phan tu list co 2 characters.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = [] #danh dau cac nuoc da di truoc do

    #ham move quan c
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        if move.pieceMoved != "--": #if user chosen "--" then do not thing else so something
            self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #swap players


class Move():
    # maps keys to values (ánh xạ khóa tới giá trị)
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    # broad dung de cung cap thong tin cho viec xet cac valid move
    def __init__(self, startSq, endSq, board):
        #khai bao cac bien thuong dung
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] #vi tri bat dau
        self.pieceCaptured = board[self.endRow][self.endCol]  #vi tri ket thuc

    # hien thong tin move ra terminal
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r,c):
        return  self.colsToFiles[c] + self.rowsToRanks[r]