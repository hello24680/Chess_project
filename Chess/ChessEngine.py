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



    def getRookMoves(self, r, c, moves, turn):
        # kiem tra row phia ben trai
        for i in range(len(self.board)):
            # bỏ qua chính bản thân nó => nếu không sẽ luôn vào elif self.board[r][c-i][0] == "b" (dong 164) và break
            if i == 0:
                continue

            if (c - i) >= 0:  # kiem tra toi bien gioi chua
                if turn == "w":  # kiem tra turn (phe cua quan co)
                    if self.board[r][c - i] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r, c - i), self.board))
                    elif self.board[r][c - i][0] == "b":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r, c - i), self.board))
                        break
                    elif self.board[r][c - i][0] == "w":  # neu quan phe minh thi chi break khong append
                        break
                elif turn == "b":
                    if self.board[r][c - i] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r, c - i), self.board))
                    elif self.board[r][c - i][0] == "w":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r, c - i), self.board))
                        break
                    elif self.board[r][c - i][0] == "b":  # neu quan phe minh thi chi break khong append
                        break
            else:
                break

        # kiem tra row phia ben phai
        for i in range(len(self.board)):
            if i == 0:
                continue

            if (c + i) <= 7:
                if turn == "w":  # kiem tra turn (phe cua quan co)
                    if self.board[r][c + i] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r, c + i), self.board))
                    elif self.board[r][c + i][0] == "b":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r, c + i), self.board))
                        break
                    elif self.board[r][c + i][0] == "w":  # neu quan phe minh thi chi break khong append
                        break
                elif turn == "b":
                    if self.board[r][c + i] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r, c + i), self.board))
                    elif self.board[r][c + i][0] == "w":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r, c + i), self.board))
                        break
                    elif self.board[r][c + i][0] == "b":  # neu quan phe minh thi chi break khong append
                        break
                else:
                    break

        # kiem tra col phia ben tren
        for i in range(len(self.board[r])):
            if i == 0:
                continue

            if (r - i) >= 0:
                if turn == "w":  # kiem tra turn (phe cua quan co)
                    if self.board[r - i][c] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r - i, c), self.board))
                    elif self.board[r - i][c][0] == "b":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r - i, c), self.board))
                        break
                    elif self.board[r - i][c][0] == "w":  # neu quan phe minh thi chi break khong append
                        break
                elif turn == "b":
                    if self.board[r - i][c] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r - i, c), self.board))
                    elif self.board[r - i][c][0] == "w":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r - i, c), self.board))
                        break
                    elif self.board[r - i][c][0] == "b":  # neu quan phe minh thi chi break khong append
                        break
                else:
                    break

        # kiem tra col phia ben duoi
        for i in range(len(self.board[r])):
            if i == 0:
                continue

            if (r + i) <= 7:
                if turn == "w":  # kiem tra turn (phe cua quan co)
                    if self.board[r + i][c] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r + i, c), self.board))
                    elif self.board[r + i][c][0] == "b":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r + i, c), self.board))
                        break
                    elif self.board[r + i][c][0] == "w":  # neu quan phe minh thi chi break khong append
                        break
                elif turn == "b":
                    if self.board[r + i][c] == "--":  # neu o trong thi append
                        moves.append(Move((r, c), (r + i, c), self.board))
                    elif self.board[r + i][c][0] == "w":  # neu quan doi phuong thi append xong break
                        moves.append(Move((r, c), (r + i, c), self.board))
                        break
                    elif self.board[r + i][c][0] == "b":  # neu quan phe minh thi chi break khong append
                        break
                else:
                    break


    def getKnightMoves(self, r, c, moves, turn):
        # huong len tren
        if (r - 2) >= 0:
            # neu chua vuot ngoai bien gioi va khong phai la vi tri cua quan dong minh dang o day
            if c + 1 <= 7 and self.board[r - 2][c + 1][0] != turn:  # sang phai
                moves.append(Move((r, c), (r - 2, c + 1), self.board))

            if c - 1 >= 0 and self.board[r - 2][c - 1][0] != turn:  # sang trai
                moves.append(Move((r, c), (r - 2, c - 1), self.board))

        # huong xuong duoi
        if (r + 2) <= 7:
            if c + 1 <= 7 and self.board[r + 2][c + 1][0] != turn:  # sang phai
                moves.append(Move((r, c), (r + 2, c + 1), self.board))

            if c - 1 >= 0 and self.board[r + 2][c - 1][0] != turn:  # sang trai
                moves.append(Move((r, c), (r + 2, c - 1), self.board))

        # huong sang trai
        if c - 2 >= 0:
            if r + 1 <= 7 and self.board[r + 1][c - 2][0] != turn:  # di xuong
                moves.append(Move((r, c), (r + 1, c - 2), self.board))

            if r - 1 >= 0 and self.board[r - 1][c - 2][0] != turn:  # di len
                moves.append(Move((r, c), (r - 1, c - 2), self.board))

        # huong sang phai
        if c + 2 <= 7:
            if r + 1 <= 7 and self.board[r + 1][c + 2][0] != turn:  # di xuong
                moves.append(Move((r, c), (r + 1, c + 2), self.board))

            if r - 1 >= 0 and self.board[r - 1][c + 2][0] != turn:  # di len
                moves.append(Move((r, c), (r - 1, c + 2), self.board))


    def getBishopMoves(self, r, c, moves, turn):
        # row di xuong

        ##col sang trai
        for i in range(len(self.board)):
            if i == 0:
                continue

            if r + i <= 7:
                if c - i >= 0:
                    if self.board[r + i][c - i] == "--":
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                    elif self.board[r + i][c - i][0] != turn:
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                        break
                    elif self.board[r + i][c - i][0] == turn:
                        break

        ##col sang phai
        for i in range(len(self.board)):
            if i == 0:
                continue

            if r + i <= 7:
                if c + i < 7:
                    if self.board[r + i][c + i] == "--":
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                    elif self.board[r + i][c + i][0] != turn:
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                        break
                    elif self.board[r + i][c + i][0] == turn:
                        break

        # row di len
        ##col sang trai
        for i in range(len(self.board)):
            if i == 0:
                continue

            if r - i >= 0:
                if c - i >= 0:
                    if self.board[r - i][c - i] == "--":
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                    elif self.board[r - i][c - i][0] != turn:
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                        break
                    elif self.board[r - i][c - i][0] == turn:
                        break

        ## col sang phai
        for i in range(len(self.board)):
            if i == 0:
                continue

            if r - i >= 0:
                if c + i <= 7:
                    if self.board[r - i][c + i] == "--":
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                    elif self.board[r - i][c + i][0] != turn:
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                        break
                    elif self.board[r - i][c + i][0] == turn:
                        break


    def getQueenMoves(self, r, c, moves, turn):
        # queen = Bishop + Rook
        self.getRookMoves(r, c, moves, turn)
        self.getBishopMoves(r, c, moves, turn)


    def getKingMoves(self, r, c, moves, turn):
        # Cac nuoc di co the cua vua
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc  # co the khai bao nhieu bien cung luc

            # kiem tra o co ton tai trong ban co
            if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                piece = self.board[new_r][new_c]

                # kiem tra neu la o trong hoac co piece doi phuong thi la nuoc di hop le
                if piece == "--" or piece[0] != turn:
                    moves.append(Move((r, c), (new_r, new_c), self.board))


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