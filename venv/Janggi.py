import pygame
from pygame.locals import *
import os

class Janggi:
    """The main pygame class for displaying the game"""
    def __init__(self):
        """Initialized the game"""
        self._running = True
        self._display_surf = None
        self._size = self.weight, self.height = 833, 927

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

    def on_event(self, event):
        """Handles game events"""
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        """Shows the current state of the game board"""
        self._display_surf.blit(self._board_image, (0, 0))
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