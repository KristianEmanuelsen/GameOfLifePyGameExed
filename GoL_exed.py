# Programmed by Kristian Emanuelsen

from random import randint # Random number generator
import pygame 
import time
import sys # To terminate the pygame with sys.exit() and use sys._MEIPASS to make exe with PyInstaller
import os

# Setting up color constants and size of cell squares
COLOR_BG = (10,10,10) # Black background color
COLOR_GRID = (0,100,240) # Blue color for the game grid
CELL_SIZE = 20 # The size of a cell square

# The cell class
class Cell:
    # Initializer for cells
    def __init__(self):
        self._alive = False
        self._neighbors = []
        self._number_of_living_neighbors = 0
        
    # Methods and functions of the cell class:

    # Sets the cell status to dead
    def set_dead(self):
        self._alive = False

    # Sets the cell status to alive
    def set_alive(self):
        self._alive = True

    # Boolean function returning true if a cell is alive or false if a cell is dead
    def is_alive(self):
        if self._alive == True:
            return True
        else:
            return False

    # Returns a green (or purple) color if a cell is alive and black color if a cell is dead (green defaults to 200 in RGB but can be changed)
    def get_status_color(self, green = 200):
        color_alive = (80, green, 80) 
        if self._alive == True:
            return color_alive
        else:
            return COLOR_BG
        
    # If a neighboring cell is alive the method adds it to the cell's neighbor-list 
    def add_neighbor(self, neighbor):
        self._neighbors.append(neighbor)


    # Counts the number of living neighbor-cells in a cell's neighbor-list, incrementing by 1
    def count_living_neighbors(self):
        self._number_of_living_neighbors = 0
        for neighbor in self._neighbors:
            if neighbor.is_alive() == True:
                self._number_of_living_neighbors += 1


    # Updates the status of a cell based on the game rules (2 or 3 living neighboring keeps the cell alive etc.)
    def update_status(self):
        if self.is_alive() == True:
            if self._number_of_living_neighbors == 2 or self._number_of_living_neighbors == 3:
                self.set_alive()
            else:
                self.set_dead()
        # If the cell was dead though, only 3 living neighbors will change it's status to alive 
        else:
            if self._number_of_living_neighbors == 3:
                self.set_alive()


# The most complex class in the program, grid. A non object oriented approach would be to use an np.array for the game grid instead
class Grid: 
    # Initializer for an empty player board grid
    def __init__(self, rows, columns):
        self._number_of_rows = rows
        self._number_of_columns = columns
        self._grid = self._make_empty_grid()

    # Methods and functions for the grid class:

    # Returns a list with an empty row for use in the _make_empty_grid() function
    def _make_empty_row(self):
        empty_row_list = []
        for column in range(self._number_of_columns):
            empty_row_list.append(None)
        return empty_row_list

    # Creates and returns an empty player board 2D grid for use in the grid initializer
    def _make_empty_grid(self):
        empty_grid = []
        for row in range(self._number_of_rows):
            empty_grid.append(self._make_empty_row())
        return empty_grid


    # Fills the empty grid with new default cells for generation 0
    def fill_empty_grid_with_cells(self):
        for row in range(self._number_of_rows):
            for column in range(self._number_of_columns):
                self.make_cell(row, column)


    # Determines the starting state of each cell in gen 0, with a 1/3 probability of starting as alive (0)
    def make_cell(self, row, col):
        new_cell = Cell()
        if randint(0, 2) == 0:
            new_cell.set_alive()
        else:
            new_cell.set_dead()
        self._grid[row][col] = new_cell


    # Returns the cell on the row, column position in the grid, controlling for None objects 
    def get_cell(self, row, col):
        if row >= self._number_of_rows or row < 0:
            return None
        if col >= self._number_of_columns or col < 0:
            return None
        return self._grid[row][col]


    # Draws the grid in pygame graphics, taking the screen and green as arguments, fetching colors for the cell class 
    def draw_grid(self, screen, green):
        for i in range(self._number_of_rows):
            for j in range(self._number_of_columns):
                color = self.get_cell(i,j).get_status_color(green) 

                # By subtracting one for width and height, it creates the grid "illusion", creating background borders around cells
                pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))


    # Iterating through the 8 neigboring cell positions for a given cell appending these neighbors to it's neighbor list (also see the add_neighbor() method in the cell class)
    def _set_neighbors(self, row, col):
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                neighbor = self.get_cell(i, j)
                if neighbor is not None and neighbor is not self.get_cell(row, col): # We need to exclude (or subtract) the "self cell", and also control for None
                    self._grid[row][col].add_neighbor(neighbor) 


    # Connecting all cells and setting their neighbors with _set_neighbors(), crucial for the next gen update
    def connect_cells(self):
        for i in range(self._number_of_rows):
            for j in range(self._number_of_columns):
                self._set_neighbors(i,j)


    # Stores all the cells in the grid in a 1D list and returns it
    def get_all_cells(self):
        all_cells = []
        for i in range(self._number_of_rows):
            for j in range(self._number_of_columns):
                this_cell = self.get_cell(i,j)
                all_cells.append(this_cell)
        return all_cells


    # Counts and returns the number of living cells in the current generation
    def number_of_living_cells(self):
        num_of_living_cells = 0
        for i in range(self._number_of_rows):
            for j in range(self._number_of_columns):
                if self.get_cell(i,j).is_alive() == True:
                    num_of_living_cells += 1
        return num_of_living_cells


# The world class
class World:
    # Initializer for drawing the full player world grid with cells included, see the grid class methods (fill and connect) 
    def __init__(self, rows, columns):
        self._generations = 0
        self._grid = Grid(rows, columns)
        self._grid.fill_empty_grid_with_cells()
        self._grid.connect_cells()

    # Methods and functions for the world class:
        
    # Draws the player world grid, see the Grid class.
    def draw_world(self, scr, gr):
        self._grid.draw_grid(scr, gr)
        # If you would like the program to print generation and number of living cells to the terminal, you can "uncheck" the code line below
        # print("Generation:", str(self._generations) + ", Living cells:", str(self._grid.number_of_living_cells()))

    # Updates the player world grid, updating the alive/dead status of all cells and generation number for the next gen
    def update_world(self):
        for cell in self._grid.get_all_cells():
            cell.count_living_neighbors()

        for cell in self._grid.get_all_cells():
            cell.update_status()

        self._generations += 1

    # Converts the cell status from alive to dead and vice versa, useful when mouse clicking on a cell (controls for None, if resizing game window etc.)
    def convert_cell(self, row, column):
        if self._grid.get_cell(row, column) is not None and self._grid.get_cell(row, column).is_alive() == True:
            self._grid.get_cell(row, column).set_dead()
        else:           
            if self._grid.get_cell(row, column) is not None:
                self._grid.get_cell(row, column).set_alive()


    # Returns a string with generation and number of living cells
    def living_cells_and_generation(self):
        cell_string = "Generation: " + str(self._generations) + ", Living cells: " + str(self._grid.number_of_living_cells())
        return cell_string
    
    # Returns generation number
    def generation_number(self):
        return self._generations
    
    # Returns number of living cells
    def living_cells_number(self):
        return self._grid.number_of_living_cells()
    

# The main program. GUI included here etc.
def GoL_exed():

    # Initializing pygame
    pygame.init() 

    # Check if we are running from a bundled exe or from source
    if getattr(sys, 'frozen', False):
        # If running from an executable
        current_directory = sys._MEIPASS
    else:
        # If running from source
        current_directory = os.path.abspath(".")

    # Path to the sound file
    sound_file_path = os.path.join(current_directory, "assets", "GoLSong.wav")
    image_file_path = os.path.join(current_directory, "assets", "PygameIcon1.png")

    # Loads the theme song music included in the folder
    pygame.mixer.music.load(sound_file_path)

    # Setting screen width, height etc.
    rows = 33 # 33
    columns = 76 # 76
    height = rows * CELL_SIZE + CELL_SIZE * 5 # Using the constant CELL_SIZE from line 11 in the program, adding 5 lines for text below the grid
    screen = pygame.display.set_mode((columns * CELL_SIZE, height), pygame.RESIZABLE) 
    screen.fill(COLOR_GRID) # Blue color
    pygame.display.set_caption("Conway's Game of Life 2025 (Emanuelsen)") # Window title


    # Changes the icon in upper left of game window loading the OldGamer.png image included
    program_icon = pygame.image.load(image_file_path)
    pygame.display.set_icon(program_icon)


    # Creates an instance object of the World class, then draws the world grid with cells included
    new_world = World(rows, columns)
    green_color = 210 # Default green color of living cells
    new_world.draw_world(screen, green_color)


    # Method for drawing text, rendering and blit-ing
    def draw_text(text, font, text_col, x, y):
        image = font.render(text, True, text_col)
        screen.blit(image, (x, y))

    # Creating some text fonts and text colors
    text_font = pygame.font.SysFont("Arial", CELL_SIZE, bold = True)
    white = (245, 240, 235)
    yellow = (250, 250, 100)
    red = (250, 30, 20)

    # Displays control scheme for manipulating transition speed and cell brightness etc.
    controls = "Spacebar to start/pause game, click on cells to convert\nLeft-arrow/a to slow down, Right-arrow/d to speed up\nUp-arrow/w to brighten cells, Down-arrow/s to darken"
    draw_text(controls, text_font, white, 0, height - (CELL_SIZE * 5))

    # Game over text 
    game_over_text = "Unfortunately, the cells live no more. Game over!"
    
    # Displays generation number and number of living cells in the bottom of game window
    draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)

    # Displaying it in pygame
    pygame.display.flip()
    pygame.display.update()

    # Repeats music and starts at 0.0 seconds of song
    pygame.mixer.music.play(-1, 0.0) 

    running = False

    # Creates a variable for game_time, between generation transitions, that can be modified by pressing keys (left/right a/d)
    game_time = 0.4

    # Main (infinite) game loop
    while True:
        for event in pygame.event.get():

            # The "x" in the upper right corner of the game window was clicked on to exit the game
            if event.type == pygame.QUIT:
                 
                screen.fill(COLOR_GRID) # Fills the screen with blue color to erase previous text
                new_world.draw_world(screen, green_color) 
                draw_text("Game over!", text_font, red, 0, height - (CELL_SIZE * 5))

                # Prints a message on screen depending on end game generation (same as quit)
                if new_world.generation_number() == 0:
                    draw_text("Ouch! The cells did not enjoy life. Generation = " + str(new_world.generation_number()) + "\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
                    
                elif new_world.generation_number() > 99 and new_world.generation_number() < 1000:
                    draw_text("Wow! The cells enjoyed life for " + str(new_world.generation_number()) + " generations. Well played!\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
        
                elif new_world.generation_number() >= 1000:
                    draw_text("Holy moly! The cells enjoyed life for " + str(new_world.generation_number()) + " generations. You must be a genius!\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
            
                else: # Cells reached generation between 1 and 99 
                    draw_text("Not bad! The cells enjoyed life for " + str(new_world.generation_number()) + " generations.\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
        
                draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                pygame.display.update()  
                running = False
                pygame.time.delay(3000) # End game screen holds for 3 seconds then quits and exits
                pygame.quit()
                sys.exit()    

            # Event for resizing the game window (cell size is not updated though)
            if event.type == pygame.VIDEORESIZE:
                screen_size = event.size
                screen = pygame.display.set_mode((screen_size), pygame.RESIZABLE)
                screen.fill(COLOR_GRID) # Blue color
                new_world.draw_world(screen, green_color)
                draw_text(controls, text_font, white, 0, height - (CELL_SIZE * 5))
                draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                pygame.display.update()


            # Events when pressing keyboard keys:
            if event.type == pygame.KEYDOWN:

                # Spacebar was pressed to start/pause the game
                if event.key == pygame.K_SPACE:                       
                    running = not running
                    new_world.draw_world(screen, green_color)
                    draw_text(controls, text_font, white, 0, height - (CELL_SIZE * 5))
                    draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                    pygame.display.update()

            # If a position on the player grid screen is clicked on, it will change the cell status (alive/dead)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                new_world.convert_cell(pos[1] // CELL_SIZE, pos[0] // CELL_SIZE)
                new_world.draw_world(screen, green_color)
                draw_text(controls, text_font, white, 0, height - (CELL_SIZE * 5))
                draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                pygame.display.update()

        screen.fill(COLOR_GRID) # Fills the screen with blue color 


        # While the game is running the game world updates to next generation in game_time transition speed 
        if running:

            # Enabling holding down the designated keys to trigger it's effect (used for all keys except spacebar)
            keys = pygame.key.get_pressed()

            # If left-arrow or 'a' is pressed it will slow down the in-game generation transitions by 0.05  
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                game_time += 0.05

            # Right-arrow or 'd' was pressed to speed up the in-game generation transitions by 0.05
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if game_time > 0.05:
                    game_time -= 0.05

            # Up-arrow or 'w' was pressed to brighten the green color of cells by 10
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if green_color < 245:
                    green_color += 10

            # Down-arrow or 's' was pressed to darken the green color of cells down to gray/purple by 10 
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if green_color > 9:
                    green_color -= 10


            # Game over if living cells = 0
            if new_world.living_cells_number() == 0:
                screen.fill(COLOR_GRID) # Fills the screen with blue color (erasing previous text)
                new_world.draw_world(screen, green_color)  
                draw_text(game_over_text, text_font, red, 0, height - (CELL_SIZE * 5))

                # Displays a message on screen depending on end game generation "scoring" (same as the quit message)
                if new_world.generation_number() == 0:
                    draw_text("Ouch! The cells did not enjoy life. Generation = " + str(new_world.generation_number()), "\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
                   
                elif new_world.generation_number() > 99 and new_world.generation_number() < 1000:
                    draw_text("Wow! The cells enjoyed life for " + str(new_world.generation_number()) + " generations. Well played!\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
        
                elif new_world.generation_number() >= 1000:
                    draw_text("Holy moly! The cells enjoyed life for " + str(new_world.generation_number()) + " generations. You must be a genius!\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
                   
                else: # Cells reached generation between 1 and 99 
                    draw_text("Not bad! The cells enjoyed life for " + str(new_world.generation_number()) + " generations.\nThank you for trying Conway's Game of Life!", text_font, white, 0, height - (CELL_SIZE * 4))
        
                draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                pygame.display.update()  
                running = False
                pygame.time.delay(3000) # End game screen holds for 3 seconds then quits and exits
                pygame.quit()
                sys.exit()    
                
            # Game loop continues
            else:
                new_world.update_world()
                new_world.draw_world(screen, green_color) 
                draw_text(controls, text_font, white, 0, height - (CELL_SIZE * 5))
                draw_text(new_world.living_cells_and_generation(), text_font, yellow, 0, height - CELL_SIZE)
                pygame.display.update()  
                time.sleep(game_time)             

GoL_exed()
