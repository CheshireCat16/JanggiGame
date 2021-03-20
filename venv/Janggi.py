import pygame
from pygame.locals import *
from JanggiGame import JanggiGame, JanggiPiece
import os

class Janggi:
    """The main pygame class for displaying the game"""
    def __init__(self):
        """Initialized the game"""
        self._running = True
        self._display_surf = None
        self._size = self.weight, self.height = 833, 927
        self._JanggiGame = JanggiGame()
        self._piece_images = {}

    def on_init(self):
        """
        Initialized pygame models and setup the displa window
        Note: Display window size equal to board game size
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        # Load images of board and game pieces
        self._board_image = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\JanggiBoard.gif").convert()
        self._blue_general = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_King.png").convert()
        self._blue_soldier = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Sa.png").convert()
        self._blue_chariot = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Cha.png").convert()
        self._blue_cannon = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Po.png").convert()
        self._blue_elephant = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Sang.png").convert()
        self._blue_horse = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Ma.png").convert()
        self._blue_guard = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Zol.png").convert()
        self._board_image = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\JanggiBoard.gif").convert()
        self._red_general = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_King.png").convert()
        self._red_soldier = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Sa.png").convert()
        self._red_chariot = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Cha.png").convert()
        self._red_cannon = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Po.png").convert()
        self._red_elephant = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Sang.png").convert()
        self._red_horse = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Ma.png").convert()
        self._red_guard = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Byung.png").convert()

    def on_event(self, event):
        """Handles game events"""
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.on_lbutton_up(event)


    def on_loop(self):
        pass

    def on_render(self):
        """Shows the current state of the game board"""
        self._display_surf.blit(self._board_image, (0, 0))

        current_board = self._JanggiGame.get_board().get_board_layout()

        # Loop through board
        for row in range(0, 10):
            for column in range(0, 9):
                piece = current_board[row][column]
                if piece is not None:
                    color = piece.get_color()
                    piece_type = piece.get_piece_type()



        pygame.display.flip()

    def on_cleanup(self):
        """Close down all pygame modules"""
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    JanggiApp = Janggi()
    JanggiApp.on_execute()