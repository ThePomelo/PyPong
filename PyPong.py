# PyPong!
# A Pong implementation written by Michael Collins

import pygame # import the pygame library
import sys	# import the sys library, we'll use this for the sys.exit() function

# define some useful constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BACKGROUND_COLOR = (80,80,80)





pygame.init() # initialize the pygame window
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) # set the size of the pygame window
pygame.display.set_caption('PyPong') # set the caption

background = pygame.Surface(window.get_size()) # create a pygame Surface and make it the same size as the window
background = background.convert() # convert the Surface to pixel format, the background is now ready to be displayed
background.fill(BACKGROUND_COLOR)
