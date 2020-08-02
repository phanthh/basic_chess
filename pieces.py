import pygame


class Bishop:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_bishop.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_bishop.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    # LATER

    def checkMove(self, board):
        return possibleBishop(self, board)


class King:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_king.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_king.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    def checkMove(self, board):
        kingMoves = [[self.pos[0]+1, self.pos[1]+1], [self.pos[0]+1, self.pos[1]-1], [self.pos[0]+1, self.pos[1]], [self.pos[0]-1, self.pos[1]+1], [
            self.pos[0]-1, self.pos[1]], [self.pos[0]-1, self.pos[1]-1], [self.pos[0], self.pos[1]+1], [self.pos[0], self.pos[1]-1]]
        possibleMoves = []
        for move in kingMoves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                if isinstance(board[move[0]][move[1]], Empty):
                    possibleMoves.append(move)
                elif board[move[0]][move[1]].side != self.side:
                    possibleMoves.append(move)

        return possibleMoves


class Knight:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_knight.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_knight.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    def checkMove(self, board):
        knightMoves = [[self.pos[0]-2, self.pos[1]+1], [self.pos[0]-1, self.pos[1]+2], [self.pos[0]+1, self.pos[1]+2], [self.pos[0]+2, self.pos[1]+1], [
            self.pos[0]+2, self.pos[1]-1], [self.pos[0]+1, self.pos[1]-2], [self.pos[0]-1, self.pos[1]-2], [self.pos[0]-2, self.pos[1]-1]]
        possibleMoves = []
        for move in knightMoves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                if isinstance(board[move[0]][move[1]], Empty):
                    possibleMoves.append(move)
                elif board[move[0]][move[1]].side != self.side:
                    possibleMoves.append(move)
        return possibleMoves


class Pawn:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_pawn.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_pawn.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    def checkMove(self, board):
        possibleMoves = []
        if self.side == 'white':
            if isinstance(board[self.pos[0]+1][self.pos[1]], Empty):
                possibleMoves.append([self.pos[0]+1, self.pos[1]])
                if self.moveCount == 0:
                    if isinstance(board[self.pos[0]+2][self.pos[1]], Empty):
                        possibleMoves.append([self.pos[0]+2, self.pos[1]])
            if self.pos[0]+1 <= 7:
                if self.pos[1]-1 >= 0:
                    if not isinstance(board[self.pos[0]+1][self.pos[1]-1], Empty):
                        if board[self.pos[0]+1][self.pos[1]-1].side == 'black':
                            possibleMoves.append(
                                [self.pos[0]+1, self.pos[1]-1])

                if self.pos[1]+1 <= 7:
                    if not isinstance(board[self.pos[0]+1][self.pos[1]+1], Empty):
                        if board[self.pos[0]+1][self.pos[1]+1].side == 'black':
                            possibleMoves.append(
                                [self.pos[0]+1, self.pos[1]+1])

        if self.side == 'black':
            if isinstance(board[self.pos[0]-1][self.pos[1]], Empty):
                possibleMoves.append([self.pos[0]-1, self.pos[1]])
                if self.moveCount == 0:
                    if isinstance(board[self.pos[0]-2][self.pos[1]], Empty):
                        possibleMoves.append([self.pos[0]-2, self.pos[1]])
            if self.pos[0]-1 >= 0:
                if self.pos[1]-1 >= 0:
                    if not isinstance(board[self.pos[0]-1][self.pos[1]-1], Empty):
                        if board[self.pos[0]-1][self.pos[1]-1].side == 'white':
                            possibleMoves.append(
                                [self.pos[0]-1, self.pos[1]-1])

                if self.pos[1]+1 <= 7:
                    if not isinstance(board[self.pos[0]-1][self.pos[1]+1], Empty):
                        if board[self.pos[0]-1][self.pos[1]+1].side == 'white':
                            possibleMoves.append(
                                [self.pos[0]-1, self.pos[1]+1])

        return possibleMoves


class Queen:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_queen.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_queen.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    def checkMove(self, board):
        return possibleBishop(self, board) + possibleRook(self, board)


class Rook:
    def __init__(self, pos, side, game):
        self.pos = pos
        self.side = side
        self.width, self.height = (420//8, 420//8)
        if self.side == 'white':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/white_rook.png'), (int(self.width*0.8), int(self.height*0.8)))
        elif self.side == 'black':
            self.img = pygame.transform.scale(pygame.image.load(
                'assets/chess/black_rook.png'), (int(self.width*0.8), int(self.height*0.8)))

        self.moveCount = 0

    def draw(self, screen):
        screen.blit(
            self.img, (self.pos[1]*self.width+100, self.pos[0]*self.height+100))

    def checkMove(self, board):
        return possibleRook(self, board)


class Empty:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, screen):
        pass


def possibleRook(obj, board):
    possibleMoves = []
    # UP
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        r = r - 1
        if r < 0:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break

    # DOWN
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        r = r + 1
        if r > 7:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break

        # RIGHT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        c = c + 1
        if c > 7:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break
    # LEFT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        c = c - 1
        if c < 0:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break

    return possibleMoves


def possibleBishop(obj, board):
    possibleMoves = []
    # UP RIGHT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        r = r - 1
        c = c + 1
        if r < 0 or c > 7:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break

    # DOWN RIGHT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        r = r + 1
        c = c + 1
        if r > 7 or c > 7:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break
    # DOWN LEFT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        r = r + 1
        c = c - 1
        if c < 0 or r > 7:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break
    # UP LEFT
    r = obj.pos[0]
    c = obj.pos[1]
    while True:
        c = c - 1
        r = r - 1
        if c < 0 or r < 0:
            break
        if isinstance(board[r][c], Empty):
            possibleMoves.append([r, c])
        else:
            if board[r][c].side == obj.side:
                break
            else:
                possibleMoves.append([r, c])
                break

    return possibleMoves
