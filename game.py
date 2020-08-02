from copy import copy, deepcopy

import pygame

from pieces import Bishop, Empty, King, Knight, Pawn, Queen, Rook


class Game:
    def __init__(self):
        pygame.init()
        SCREEN_WIDTH = 600
        SCREEN_HEIGHT = 600
        size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.set_caption('Chess')

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        self.bg = pygame.transform.scale(pygame.image.load(
            'assets/chess/board_alt.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.backArrow = pygame.transform.scale(
            pygame.image.load('assets/arrow.png'), (40, 40))
        self.running = False

        self.start_setup()

        self.showingMove = False
        self.possibleMoves = []
        self.clickedPiece = None
        self.back = False

        self.textFont = pygame.font.SysFont('Ariel', 50)
        self.turn = 'white'
        self.text = self.textFont.render(
            f'{self.turn} turn!'.capitalize(), False, (255, 255, 255))

        self.gameOver = False
        self.previousBoard = None
        self.winner = None

    def start_setup(self):
        # Setting up the board in the beginning

        self.gameOver = False
        self.board = [[Empty([y, x])
                       for x in range(8)] for y in range(8)]
        self.board[0][0] = Rook([0, 0], 'white', self)
        self.board[0][1] = Knight([0, 1], 'white', self)
        self.board[0][2] = Bishop([0, 2], 'white', self)
        self.board[0][3] = King([0, 3], 'white', self)
        self.board[0][4] = Queen([0, 4], 'white', self)
        self.board[0][5] = Bishop([0, 5], 'white', self)
        self.board[0][6] = Knight([0, 6], 'white', self)
        self.board[0][7] = Rook([0, 7], 'white', self)

        for i in range(8):
            self.board[1][i] = Pawn([1, i], 'white', self)
            self.board[6][i] = Pawn([6, i], 'black', self)

        self.board[7][0] = Rook([7, 0], 'black', self)
        self.board[7][1] = Knight([7, 1], 'black', self)
        self.board[7][2] = Bishop([7, 2], 'black', self)
        self.board[7][3] = King([7, 3], 'black', self)
        self.board[7][4] = Queen([7, 4], 'black', self)
        self.board[7][5] = Bishop([7, 5], 'black', self)
        self.board[7][6] = Knight([7, 6], 'black', self)
        self.board[7][7] = Rook([7, 7], 'black', self)

    def run_game(self):
        self.running = True
        # Main game loop
        while self.running:
            self.process_events()
            self.draw_game()
            # DEBUG
            # print('showing move: ', self.showingMove)
            # print('possible move:', self.possibleMoves)
            # print(' ------------------------------ ')
            self.clock.tick(60)
        pygame.quit()

    def draw_game(self):
        # Main display draw
        self.screen.blit(self.bg, (0, 0))
        for r_piece in self.board:
            for piece in r_piece:
                piece.draw(self.screen)
        self.screen.blit(self.backArrow, (460, 5))
        if self.showingMove:
            self.drawPossibleMoves()
        self.screen.blit(self.text, (90, 10))
        pygame.display.update()

    def process_events(self):
        # Main events handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickOnScreen()
        self.checkForEnd()
        if self.gameOver:
            self.text = self.textFont.render(
                f'{self.winner} win!'.capitalize(), False, (255, 255, 255))

    def checkForEnd(self):
        l = []
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    l.append(piece.side)
        if len(l) == 1:
            self.gameOver = True
            self.winner = l[0]

    def clickOnScreen(self):
        mouse_pos = pygame.mouse.get_pos()
        # Check if clicked inside the board
        if mouse_pos[0] > 90 and mouse_pos[0] < 510 and mouse_pos[1] > 90 and mouse_pos[1] < 510:
            board_pos = self.PixelToBoardPos(mouse_pos)
            print('Clicked position:', board_pos)
            # Showing chess move and logic
            self.gameLogic(board_pos)
        if mouse_pos[0] > 460 and mouse_pos[0] < 500 and mouse_pos[1] > 5 and mouse_pos[1] < 45:
            # Click on the back button
            self.backLogic()

    def backLogic(self):
        if not self.back:
            self.turn = 'white' if self.turn == 'black' else 'black'
            self.text = self.textFont.render(
                f'{self.turn} turn!'.capitalize(), False, (255, 255, 255))
            self.back = True
            self.board = self.previousBoard
        self.showingMove = False
        self.clickedPiece = None
        self.possibleMoves = []

    def gameLogic(self, board_pos):
        # Main game Logic
        if self.showingMove:
            if board_pos in self.possibleMoves:
                # Save previous board
                self.previousBoard = [[piece for piece in row]
                                      for row in self.board]
                # Move piece
                self.movePiece(
                    self.board, self.clickedPiece.pos, board_pos)

                # Special case for the pawn
                if isinstance(self.board[board_pos[0]][board_pos[1]], Pawn):
                    if board_pos[0] == 0 or board_pos[0] == 7:
                        self.board[board_pos[0]][board_pos[1]] = Queen(
                            [board_pos[0], board_pos[1]], self.board[board_pos[0]][board_pos[1]].side, self)

                self.back = False
                self.showingMove = False
                self.possibleMoves = []
                self.clickedPiece = None

                # Switch Turn
                self.turn = 'white' if self.turn == 'black' else 'black'
                # Change text
                self.text = self.textFont.render(
                    f'{self.turn} turn!'.capitalize(), False, (255, 255, 255))
            else:
                # When Not click on possible move
                self.clickOnPieceHandler(board_pos)
        else:
            # When game is not showing possible move
            self.clickOnPieceHandler(board_pos)

    def clickOnPieceHandler(self, board_pos):
        if isinstance(self.board[board_pos[0]][board_pos[1]], Empty):
            # Clicked on Empty
            pass
        elif self.board[board_pos[0]][board_pos[1]].side != self.turn:
            # Clicked on your piece but not your turn
            pass
        else:
            # Clicked on your piece
            pieceChosen = self.board[board_pos[0]][board_pos[1]]
            # Check for all move possible
            self.possibleMoves = pieceChosen.checkMove(self.board)
            # Check whether the king is being checkmated:
            if self.beingCheck(self.board, self.turn):
                # Return move that available
                self.possibleMoves = self.movesFilter(
                    self.possibleMoves, board_pos, self.turn)
            self.showingMove = True
            self.clickedPiece = pieceChosen

    def beingCheck(self, board, turn):
        # Current white turn so check for black being checked or not ?
        allOpponentMoves = []
        opponentPieces = []
        kingPos = []
        opponent = 'white' if turn == 'black' else 'black'
        for row in board:
            for piece in row:
                if isinstance(piece, Empty):
                    pass
                else:
                    if piece.side == opponent:
                        opponentPieces.append(piece)
                    else:
                        if isinstance(piece, King):
                            kingPos = piece.pos
        for piece in opponentPieces:
            allOpponentMoves = allOpponentMoves + piece.checkMove(board)
        if kingPos in allOpponentMoves:
            return True
        return False

    def movesFilter(self, availableMoves, board_pos, turn):
        filteredMoves = []
        pieceClicked = copy(self.board[board_pos[0]][board_pos[1]])
        for move in availableMoves:
            testBoard = [[piece for piece in row] for row in self.board]

            testBoard[board_pos[0]][board_pos[1]] = Empty(
                [board_pos[0], board_pos[1]])
            testBoard[move[0]][move[1]] = pieceClicked
            testBoard[move[0]][move[1]].pos = [move[0], move[1]]
            if not self.beingCheck(testBoard, turn):
                filteredMoves.append(move)

        return filteredMoves

    def movePiece(self, board, pos1, pos2):
        board[pos2[0]][pos2[1]] = copy(board[pos1[0]][pos1[1]])
        board[pos1[0]][pos1[1]] = Empty([pos1[0], pos1[1]])
        board[pos2[0]][pos2[1]].pos = [pos2[0], pos2[1]]
        board[pos2[0]][pos2[1]].moveCount += 1

    def drawPossibleMoves(self):
        for move in self.possibleMoves:
            pygame.draw.circle(self.screen, (255, 0, 0), (90 + int(
                (move[1]+1/2)*420//8), 90 + int((move[0]+1/2)*420//8)), 420//32)
        pygame.draw.circle(self.screen, (0, 0, 255), (90 + int(
            (self.clickedPiece.pos[1]+1/2)*420//8), 90 + int((self.clickedPiece.pos[0]+1/2)*420//8)), 420//16, 4)

    def PixelToBoardPos(self, mouse_pos):
        return [(mouse_pos[1]-90)//(420//8), (mouse_pos[0]-90)//(420//8)]


game = Game()
game.run_game()
