import pygame
from pygame.locals import *
from JanggiGame import JanggiGame, JanggiPiece
import os
from math import sqrt

class Janggi:
    """The main pygame class for displaying the game"""
    def __init__(self):
        """Initialized the game"""
        self._running = True
        self._display_surf = None
        self._size = self._weight, self._height = 1133, 927
        self._JanggiGame = JanggiGame()
        self._piece_images = {"blue":{}, "red": {}}
        self._clicked_piece = None
        self._valid_move_img = None
        self._status_bar_img = None
        self._current_side_font = None
        self._pass_text = None
        self._blue_side_text = None
        self._red_side_text = None

    def on_init(self):
        """
        Initialized pygame models and setup the displa window
        Note: Display window size equal to board game size
        """
        # Start up pygame and the game display
        pygame.init()
        self._running = True
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # This surface is used to draw semi-transparent figures
        self._transparent_surf = pygame.Surface((1133, 927), pygame.SRCALPHA)
        self._transparent_surf.fill((255, 255, 255, 0))
        # Set the game window name
        pygame.display.set_caption("Janggi - Korean Chess")

        # Load images of board and game pieces
        self._board_image = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\JanggiBoard.gif").convert()
        self._piece_images["blue"]["General"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_King.png").convert()
        self._piece_images["blue"]["Guard"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Sa.png").convert()
        self._piece_images["blue"]["Chariot"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Cha.png").convert()
        self._piece_images["blue"]["Cannon"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Po.png").convert()
        self._piece_images["blue"]["Elephant"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Sang.png").convert()
        self._piece_images["blue"]["Horse"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Ma.png").convert()
        self._piece_images["blue"]["Soldier"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Green_Zol.png").convert()
        self._piece_images["red"]["General"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_King.png").convert()
        self._piece_images["red"]["Guard"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Sa.png").convert()
        self._piece_images["red"]["Chariot"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Cha.png").convert()
        self._piece_images["red"]["Cannon"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Po.png").convert()
        self._piece_images["red"]["Elephant"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Sang.png").convert()
        self._piece_images["red"]["Horse"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Ma.png").convert()
        self._piece_images["red"]["Soldier"] = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\Red_Byung.png").convert()
        self._status_bar_img = pygame.image.load(r"C:\Users\John\OneDrive\Documents\Python Programs\JanggiGame\JanggiPieces\StatusBar.png").convert()

        # Set up font to show current player and menu
        pygame.font.init()
        self._current_side_font = pygame.font.SysFont("Sans", 40)
        self._blue_side_text = self._current_side_font.render("Blue Turn", False, (0, 0, 255))
        self._red_side_text = self._current_side_font.render("Red Turn", False, (255, 0, 0))
        pass_button_font = pygame.font.SysFont("Sans", 25)
        self._pass_text = pass_button_font.render("Pass", False, (0, 0, 0))

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
        # Display the game board
        self._display_surf.blit(self._board_image, (0, 0))
        self._display_surf.blit(self._status_bar_img, (834, 0))

        # Loop through board and put pieces in the correct location
        current_board = self._JanggiGame.get_board().get_board_layout()
        for row in range(0, 10):
            for column in range(0, 9):
                piece = current_board[row][column]
                if piece is not None:
                    color = piece.get_color()
                    piece_type = piece.get_piece_type()
                    self._display_surf.blit(self._piece_images[color][piece_type], (column*94-20, row*94-13))

        # Draw valid moves and selected piece if a piece has been clicked
        if self._clicked_piece is not None:
            valid_moves = self._clicked_piece.find_valid_moves(self._JanggiGame.get_board())
            new_surface = self._transparent_surf.copy()
            for row, column in valid_moves:
                pygame.draw.circle(new_surface, (108, 253, 255), (column * 94 + 41, row * 94 + 41), 20)
            row, column = self._clicked_piece.get_location()
            pygame.draw.circle(new_surface, (255, 255, 77), (column * 94 + 41, row * 94 + 41), 12)
            new_surface.set_alpha(150)
            self._display_surf.blit(new_surface, (0, 0))

        # Show text for current side
        if self._JanggiGame.get_current_side().get_color() == "blue":
            self._display_surf.blit(self._blue_side_text, (880, 205))
        else:
            self._display_surf.blit(self._red_side_text, (880, 205))

        # Draw a rectangle for the pass button
        pygame.draw.rect(self._display_surf, (0, 0, 0), Rect(1030, 200, 60, 60), width=2, border_radius=4)
        self._display_surf.blit(self._pass_text, (1038, 213))

        # Render the board
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

    def on_lbutton_up(self, event):
        """Handles a click on a peice"""
        clicked_spot = None
        click_box    = 0
        # Get the coordinates of the click
        x_click, y_click = event.pos

        # Get the current board for checking click locations
        current_board = self._JanggiGame.get_board().get_board_layout()

        # Find the row and column that was clicked
        for row in range(0, 10):
            for column in range(0, 9):
                # Get the coordinates of the current location
                x_loc = column*94+39
                y_loc = row*94+39
                # Calculate the distance between the center and the click
                distance = sqrt((x_loc-x_click)**2 + (y_loc-y_click)**2)
                # Find what is at the location
                piece = current_board[row][column]
                # Set the click box based on the size of the piece at the location
                if piece is not None:
                    piece_type = piece.get_piece_type()
                    if piece_type == "Horse" or piece_type == "Cannon" \
                            or piece_type == "Chariot" or piece_type == "Elephant":
                        click_box = 40
                    elif piece_type == "General":
                        click_box = 47
                    else:
                        click_box = 32
                # Click box size is 42 if location is empty
                else:
                    click_box = 47

                # Check whether or not the click is within the click box and exit for
                if distance < click_box:
                    clicked_spot = row, column
                    break

        # Check that there was a valid click
        if clicked_spot is not None:
            # Handle the case where a piece has already been picked up
            if self._clicked_piece is not None:
                piece_location = self._clicked_piece.get_location()
                # Put the piece down if the same spot is clicked again
                if piece_location == clicked_spot:
                    self._clicked_piece = None
                # Try the move otherwise
                else:
                    move_success = self._JanggiGame.make_move(piece_location, clicked_spot)
                    # If the move is successful, reset the current clicked piece
                    if move_success is True:
                        self._clicked_piece = None
            # Handle the case where no piece has been picked up
            else:
                clicked_piece = current_board[clicked_spot[0]][clicked_spot[1]]
                # Make sure a piece was clicked
                if clicked_piece is not None:
                    if clicked_piece.get_color() == self._JanggiGame.get_current_side().get_color():
                        self._clicked_piece = clicked_piece
        # Check if UI buttons were clicked
        else:
            if 1090 >= x_click and x_click >= 1030 and 260 >= y_click and y_click>= 200:
                self._JanggiGame.make_move((9, 9), (9, 9))





if __name__ == "__main__":
    JanggiApp = Janggi()
    JanggiApp.on_execute()