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

        #dictionary ánh xạ 1 ký tự với 1 hàm để dùng trong getAllPossibleMoves(self)
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

    #move pieces func
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        if move.pieceMoved != "--": #if user chosen "--" then do not thing else so something
            self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #swap players

    #undoMove func
    def undoMove(self):
        moveUndo = self.moveLog.pop() #lay doi tuong move truoc do
        #reverse lai make move
        self.board[moveUndo.endRow][moveUndo.endCol] = moveUndo.pieceCaptured
        self.board[moveUndo.startRow][moveUndo.startCol] = moveUndo.pieceMoved
        self.whiteToMove = not self.whiteToMove

    #all validmoves not include checks func
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = [] #the list of valid moves
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #first letter of the character ([0])
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #type of piece
                    self.moveFunctions[piece](r,c,moves,turn) #call valid func according to each type of piece

        return moves


    #valid pawnMoves
    def getPawnMoves(self, r,c,moves,turn):
        #check vi tri 2 cot bên xem co nuoc di ăn chéo không
        ##check cot ben trai
        if c-1 >= 0: #check trong trường hop con tốt đang ở cột 0 và hàng cuối 7 hay ko (ko thì sẽ báo lỗi)
            if turn == "b"  and r+1 <= 7:
                leftCol = self.board[r+1][c-1]
                if leftCol != "--" and leftCol[0] == "w":
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                    #them hieu ung nền đỏ vào
            elif turn == "w"  and r-1 >= 0:
                leftCol = self.board[r-1][c-1]
                if leftCol != "--" and leftCol[0] == "b":
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                    #them hieu ung nền đỏ vào


        ##check cot ben phai
        if c+1 <= 7: #check trong trường hop con tốt đang ở cột 7 và hàng cuối 7 hay ko (ko thì sẽ báo lỗi)
            if turn == "b" and r+1 <= 7:
                leftCol = self.board[r + 1][c+1]
                if leftCol != "--":
                    moves.append(Move((r, c), (r + 1,c+1), self.board))
                    # them hieu ung nền đỏ vào
            elif turn == "w" and r-1 >= 0:
                leftCol = self.board[r-1][c+1]
                if leftCol != "--":
                    moves.append(Move((r, c), (r - 1, c+1), self.board))
                    # them hieu ung nền đỏ vào


        #check vị trí đặc biệt: vị trí ban đâu được đi 2 bước thẳng
        ##check vi tri bat dau cua black Pawn
        if turn == "b" and  r == 1: #loi1: r==2
            if self.board[r+2][c] == "--":
                moves.append(Move((r, c), (r+2,c), self.board))

        ##check vi tri bat dau cua white Pawn
        if turn == "w" and  r == 6:
            if self.board[r-2][c] == "--":
                moves.append(Move((r, c), (r-2,c), self.board))

        #check nước đi thông thường: đi được 1 bước thẳng
        if turn == "b" and r+1 <= 7:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
        elif turn == "w" and r-1 >= 0: #co loi lap r == 6
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))


    def getRookMoves(self, r,c,moves,turn):
        pass

    def getKnightMoves(self, r,c,moves,turn):
        pass

    def getBishopMoves(self, r,c,moves,turn):
        pass

    def getQueenMoves(self, r,c,moves,turn):
        pass

    def getKingMoves(self, r,c,moves,turn):
        pass


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

        # move id to use in overide equal method
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    # overide equal method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # hien thong tin move ra terminal
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r,c):
        return  self.colsToFiles[c] + self.rowsToRanks[r]