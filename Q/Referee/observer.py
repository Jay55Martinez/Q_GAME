import sys
sys.path.insert(0, '../Common')
from game_state import *
from json_io import *
import json
import pygame
import os

#         ___  _                                  
#        / _ \| |__  ___  ___ _ ____   _____ _ __ 
#       | | | | '_ \/ __|/ _ \ '__\ \ / / _ \ '__|
#       | |_| | |_) \__ \  __/ |   \ V /  __/ |   
#        \___/|_.__/|___/\___|_|    \_/ \___|_|   

# The Observer class contains states of games. The referee updates the observer
# with a new state after each players turn. 

# - saves states it recieves from referee as pdfs
# - displays the states in a gui 
#   - user can select next and previous from the current state
#   - user can save the state as a json

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the images folder
relative_path_to_images = '../Other/pics/'

# Construct the absolute path to the images folder
PATH_TO_IMAGES = os.path.join(script_dir, relative_path_to_images)
SCORE_SPACING = 20
SCORE_TEXT_SIZE = 25
BUTTON_TEXT_SIZE = 20

class Observer:
    
    def __init__(self):
        pygame.init()
        self.row = 1280
        self.column = 900
        pygame.display.set_caption('Observer')
        self.screen = pygame.display.set_mode([self.row, self.column], flags=pygame.HIDDEN)
        self.clock = pygame.time.Clock()
        self.clock.tick(1)
        self.curr_spot = 0
        self.l_of_state = []
        self.is_game_over = False
    
      
    def update_game_over(self, gameover):
        """Changes the field is_game_over of this observer to gameover

        Args:
            gameover (bool): True if the game is over False if it is not
        """
        self.is_game_over = gameover
    
    
    def get_list_of_state(self):
        """Getter method for list of states

        Returns:
            GameState[]: list of game states
        """
        return self.l_of_state


    def update_state(self, state):
        """Appends the given GameState to the l_of_state and then renders that state as an image

        Args:
            state (GameState): the GameState that will be added and rendered as a png
        """
        self.l_of_state.append(state)
        self.save_state()
        
        
    def save_to_tmp(self):
        """saves the current gamestate as an png image to the directory Tmp/
        """
        self.save_path(str(len(self.l_of_state) - 1), 'Tmp/')
        
        
    def save_path(self, name, path):
        """saves the current gamestate as an png image to the given file location

        Args:
            name (str): the name that the file will be saved as 
            path (str): the path that the file will be saved to
        """
        if not os.path.exists(path):  
            os.mkdir(path)
        if not os.path.exists(path + name + '.png'):
            f = open(path + name + '.png', "a")
            f.close()
        pygame.image.save(self.screen, path + name + '.png')
    
    
    def save_state(self):
        """renders the current gamestate to a gui window and then saves it as a png
        """
        self.update_window()
        self.save_to_tmp()
        
        
    def update_window(self):
        """Renders the board at the curr_spot 
        """
        # Clear the screen
        self.screen.fill((0, 0, 0))
        self.renders_board()
        self.add_player_labels_to_window(self.update_player_score_labels())
        
        
    def get_current(self):
        """Returns the stored state at the index of the curr_spot

        Returns:
            GameState: The GameState at the the index of curr_spot
        """
        return self.l_of_state[self.curr_spot]


    def show_current(self):
        """Displays the png of the state that the observer is currently observing
        """
        image_file = str(self.curr_spot) + ".png"
        current_image = pygame.transform.scale(pygame.image.load("Tmp/" + image_file), (self.row, self.column))
        self.screen.blit(current_image, (0, 0))


    def show_previous(self):
        """Displays the previouse gamestate by subtracting 1 to curr_spot
        if there is no states behind then nothing happens
        """
        if not self.curr_spot <= 0:
            self.curr_spot -= 1
            self.show_current()


    def show_next(self):
        """Displays the next gamestate by adding 1 to curr_spot if there
        is no next state then nothing happens
        """
        if not self.curr_spot >= len(self.l_of_state) - 1:
            self.curr_spot += 1
            self.show_current()
      
            
    def get_last_state(self):
        """Gets the last state in this l_of_states

        Returns:
            GameState: the last gamestate in l_of_states
        """
        return self.l_of_state[len(self.l_of_state) - 1]


    def save_file_path(self, name, path):
        """Saves the state at the curr_spot as a JState to the given file path and name

        Args:
            name (str): name of the file
            path (str): the path of the file
        """
        selected_state = self.get_current()
        jstate = Json_io.to_j_state(selected_state)
        file_path = path + name + '.json'
        try:
            with open(file_path, "a") as f:
                json.dump(jstate, f)
        except Exception as e:
            print("Error while saving the file:", str(e))
         
            
    def renders_board(self):
        """Renders the Pieces on the board using pygame
        """
        image_size = 50
        offset_x = image_size /2
        offset_y = image_size /2
        file_path = PATH_TO_IMAGES
        center_row = self.row/2
        center_column = self.column/2
        
        for row in range(self.get_last_state().board.row_offset, len(self.get_last_state().board.pieces[0]) - abs(self.get_last_state().board.row_offset)):
            for column in range(self.get_last_state().board.column_offset, len(self.get_last_state().board.pieces) - abs(self.get_last_state().board.column_offset)):
                tile_allignment_row = center_row + image_size * row
                tile_allignment_column = center_column + image_size * column
                
                # get the image for the corresponding Piece
                file_for_piece = self._get_image_for_piece(self.get_last_state().board.get(Position(row, column)))
                
                # attempts to place the tile image on the view
                if file_for_piece:
                    piece_image = pygame.transform.scale(pygame.image.load(file_path + file_for_piece), (image_size, image_size))
                    self.screen.blit(piece_image, (tile_allignment_row - offset_x, tile_allignment_column - offset_y))


    def _get_image_for_piece(self, piece):
        """Helper method gets the image coresponding to the Piece

        Args:
            piece (Piece): the piece that will be used to find the image

        Returns:
            str: file name of the image that matches the piece
        """
        if piece == Piece('board', 'board'):
            return None
        
        l_of_images = [['pic_0.png', 'pic_1.png', 'pic_2.png', 'pic_3.png', 'pic_4.png', 'pic_5.png'],
                    ['pic_6.png', 'pic_7.png', 'pic_8.png', 'pic_9.png', 'pic_10.png', 'pic_11.png'],
                    ['pic_12.png', 'pic_13.png', 'pic_14.png', 'pic_15.png', 'pic_16.png', 'pic_17.png'],
                    ['pic_18.png', 'pic_19.png', 'pic_20.png', 'pic_21.png', 'pic_22.png', 'pic_23.png'],
                    ['pic_24.png', 'pic_25.png', 'pic_26.png', 'pic_27.png', 'pic_28.png', 'pic_29.png'],
                    ['pic_30.png', 'pic_31.png', 'pic_32.png', 'pic_33.png', 'pic_34.png', 'pic_35.png'],]
        
        return l_of_images[piece.shape.value - 1][piece.color.value -1] # -1 bc enum index starts at 1
    

    def update_player_score_labels(self):
        """Updates/creates the score labels for each player if the player is eliminated then the lable color will be red else the label color is greeen

        Returns:
            pygame.label[]: list of pygame labels for each player in the game
        """
        score_font = pygame.font.Font(None, SCORE_TEXT_SIZE)
        not_eliminated_label_color = (0, 212, 0) # GREEN
        eliminated_label_color = (255, 0, 0) # RED
        current_player_label_color = (255, 255, 0) #YELLOW
        
        # create player score labels
        return self._set_player_label(score_font, not_eliminated_label_color, eliminated_label_color, current_player_label_color)
    
    
    def _set_player_label(self, font, not_elim_color, elim_color, curr_color):
        """Helper method sets the lable for each of the players

        Args:
            font (Font): pygame font
            not_elim_color (Color): the color that the non-eliminated players labels will be
            elim_color (Color): the color that the eliminated players lable will be
            curr_color (Color): the color that the current player lable will be

        Returns:
            pygame.Label[]: list of pygame.Labels
        """
        l_player_labels = []
        for player in self.get_last_state().players + self.get_last_state().eliminated_players:
            if self.get_last_state().current_player == player and player.won_game:
                l_player_labels.append(font.render(f'{player.name} : {player.score} : WINNER', True, curr_color))
            elif player.won_game:
                l_player_labels.append(font.render(f'{player.name} : {player.score} : WINNER', True, not_elim_color))
            elif self.get_last_state().current_player == player:
                l_player_labels.append(font.render(f'{player.name} : {player.score}', True, curr_color))
            elif self.get_last_state()._player_eliminated(player.name):
                l_player_labels.append(font.render(f'{player.name} : {player.score}', True, elim_color))
            else:
                l_player_labels.append(font.render(f'{player.name} : {player.score}', True, not_elim_color))
        return l_player_labels
    
    
    def add_player_labels_to_window(self, l_player_labels):
        """Displays the player score labels on the window

        Args:
            l_player_labels (pygame.Label[]): the list of labels to be displayed
        """
        x_placement = 0
        y_placement = 0
        for label in l_player_labels:
            self.screen.blit(label, (x_placement, y_placement))
            y_placement += SCORE_SPACING
        
        
    def render_observer(self):
        """Renders the gui for the Observer
        """
        self.screen = pygame.display.set_mode((self.row, self.column), flags=pygame.SHOWN)
        font = pygame.font.Font(None, SCORE_TEXT_SIZE)
        
        ## Initalizing buttons
        next_button = Button(self.row - 40, self.column/2, 40, 20, "Next")
        previous_button = Button(20, self.column/2, 40, 20, "Previous")
        save_button = Button(self.row/2, self.column - 40, 40, 20, "Save")
        text_box = TextBox(self.row/2 + 60, self.column - 40, 200, 20)
        
        end_observer = True
        while end_observer:
            # Checks if there is an interaction with the textbox
            self.show_current()
            text_box.draw(self.screen)
            next_button.draw(self.screen)
            previous_button.draw(self.screen)
            save_button.draw(self.screen)

            #Checks if there is a left click on a next, previous, or save Button
            for ev in pygame.event.get():
                text_box.event_handler(ev)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: 
                    pos = pygame.mouse.get_pos()
                    if next_button.clicked(pos):
                        self.show_next()
                    elif previous_button.clicked(pos):
                        self.show_previous()
                    elif save_button.clicked(pos):
                        file_path = text_box.return_text()
                        if os.path.exists(file_path):
                            self.save_file_path(str(self.curr_spot), file_path)
                        else:
                            text = font.render('invalid file path', True, (255, 255, 255))
                            self.screen.blit(text, (self.column/2, 0))
                elif ev.type == pygame.QUIT:
                    end_observer = False
                
            pygame.display.flip()
            
            
#        ____         ____                        _____           _     
#       |  _ \ _   _ / ___| __ _ _ __ ___   ___  |_   _|__   ___ | |___ 
#       | |_) | | | | |  _ / _` | '_ ` _ \ / _ \   | |/ _ \ / _ \| / __|
#       |  __/| |_| | |_| | (_| | | | | | |  __/   | | (_) | (_) | \__ \
#       |_|    \__, |\____|\__,_|_| |_| |_|\___|   |_|\___/ \___/|_|___/
#              |___/   
                                               
# Button class creates buttons that can be displayed and interacted with on a pygame window
# TextBox class creates a text box that can be displayed and interacted with on a pygame window

class Button:
    def __init__(self, x, y, width, height, button_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, BUTTON_TEXT_SIZE)
        self.button_text = button_text
        self.color = (128, 128, 128)

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)
        text = self.font.render(self.button_text, True, (255, 255, 255))
        rect_text = text.get_rect(center=self.rect.center)
        canvas.blit(text, rect_text)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(None, BUTTON_TEXT_SIZE)
        
    def event_handler(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            self.active = self.rect.collidepoint(ev.pos)
        elif ev.type == pygame.KEYDOWN and self.active:
            if ev.key == pygame.K_BACKSPACE and len(self.text) > 0:
                self.text = self.text[:-1]
            else:
                self.text += ev.unicode
    
    def draw(self, canvas):
        pygame.draw.rect(canvas, (255, 255, 255), self.rect, 2)
        text = self.font.render(self.text, True, (255, 255, 255))
        canvas.blit(text, (self.rect.x + 5, self.rect.y + 5))
    
    def return_text(self):
        return self.text