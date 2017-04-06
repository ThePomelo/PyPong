# PyPong!
# A Pong implementation written by Michael Collins

import pygame # import the pygame library
import sys	# import the sys library, we'll use this for the sys.exit() function

# define some useful constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BACKGROUND_COLOR = (80,80,80)
LINE_COLOR = (240,240,240)
BAR_COLOR = (240,240,240)
BALL_COLOR = (240,240,240)
BAR_LENGTH = 40
BAR_SPEED = 10
BALL_SIZE = 10
FPS = 30


pygame.init() # initialize the pygame window
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) # set the size of the pygame window
pygame.display.set_caption('PyPong') # set the caption

background = pygame.Surface(window.get_size()) # create a pygame Surface and make it the same size as the window
background = background.convert() # convert the Surface to pixel format, the background is now ready to be displayed
background.fill(BACKGROUND_COLOR) # Fill the background with the background color
pygame.draw.rect(background,LINE_COLOR,pygame.Rect((0,0),(WINDOW_WIDTH-1,WINDOW_HEIGHT-1)),2) # Draw the line around the edge of the player field, it's a Rect with top left corner at (1,1), width and height are 2 less than the screen, and the thickness of the border is 2
pygame.draw.line(background,LINE_COLOR,(WINDOW_WIDTH/2,0),(WINDOW_WIDTH/2,WINDOW_HEIGHT),2) # Draw the middle line, starting at the top middle of the screen to the bottom middle, thickness 2

class Ball: # A class for the Ball
	def __init__(self,x = WINDOW_WIDTH/2,y = WINDOW_HEIGHT/2,size = BALL_SIZE, xspeed=0,yspeed=0): # this function is automatically called whenever we create a Ball
		self.x = x	# x coordinate of the midpoint of the ball
		self.y = y # y coordinate of the midpoint of the ball
		self.size = size # side length of the ball
		self.xspeed = xspeed # speed of the ball in the x direction
		self.yspeed = yspeed # speed of the ball in the y direction

		self.surface = pygame.Surface((BALL_SIZE,BALL_SIZE)); # initialize square surface of size BALL_SIZE
		self.surface = self.surface.convert() # convert to pixel array
		self.surface.fill(BALL_COLOR) # fill the surface with the color BALL_COLOR

	def reset(self,direction): # Reset the ball if a player scores
		self.x = WINDOW_WIDTH/2 # set the ball in the middle of the field
		self.y = WINDOW_HEIGHT/2
		self.yspeed = 9 # give it some y-speed

		if direction == 'left': # if the left player scored, send the ball to the left
			self.xspeed = -7
		elif direction == 'right': # if the right player scored, send the ball to the right
			self.xspeed = 7
		else:
			self.xspeed = 0 # If no direction is given, set the x speed to 0

	def move(self,new_xspeed = None, new_yspeed = None): # Move the ball the appropriate amount for one time tick
		if new_xspeed != None: # If new values of the speeds are given, set them
			self.xspeed = new_xspeed
		if new_yspeed != None:
			self.yspeed = new_yspeed

		if self.xspeed != 0 or self.yspeed != 0: # If the speeds are both 0, we don't need to move
			self.x += self.xspeed # Otherwise, advance the ball
			self.y += self.yspeed

			if self.x - BALL_SIZE/2 < 0: # If the ball hits the left wall, reset the ball and send it right
				self.reset('right')
			elif self.x + BALL_SIZE/2 > WINDOW_WIDTH: # If the ball hits the right wall, reset the ball and send it left
				self.reset('left')

			if self.y - BALL_SIZE/2 < 0: # If the ball hits the top or bottom, reverse its y-speed
				self.y *= -1
				self.yspeed *= -1
			elif self.y + BALL_SIZE/2 > WINDOW_HEIGHT:
				self.y = WINDOW_HEIGHT - (self.y - WINDOW_HEIGHT)
				self.yspeed *= -1


class Bar: # A class for the bars the players will use to defend their goals
	def __init__(self,x,y,length=BAR_LENGTH): # This function is automatically called when we create a new bar, it takes in values for the position and length and initializes these values in our new bar
		self.x = x # The x coordinate of the midpoint of the bar
		self.y = y # The y coordinate of the midpoint of the bar
		self.length = length # length of the bar
		self.speed = 0 # current speed of the bar

		self.surface = pygame.Surface((10,BAR_LENGTH))
		self.surface = self.surface.convert()
		self.surface.fill(BAR_COLOR)

	def move(self,new_speed=None): # This function moves the bar the appropriate amount for one time tick, it also lets you change the speed of the bar
		if new_speed != None:
			self.speed = new_speed # Change the speed of the bar, if a new speed was given

		if self.speed != 0:
			self.y += self.speed # Move the bar vertically

			if self.y + self.length/2 > WINDOW_HEIGHT: # Check if the bar has moved below the bottom of the window
				self.y = WINDOW_HEIGHT - self.length/2 # If so, move it back onto the screen
				self.speed = 0 # And set its speed to 0

			elif self.y - self.length/2 < 0: # Check if the bar has moved above the top of the window
				self.y = self.length/2 # If so, move it back onto the screen
				self.speed = 0


bar1 = Bar(10,WINDOW_HEIGHT/2) # Create the bar on the left side of the screen
bar2 = Bar(WINDOW_WIDTH-10,WINDOW_HEIGHT/2) # Create the bar on the right side of the screen
ball = Ball(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,BALL_SIZE,7,9)

clock = pygame.time.Clock() # create the clock we'll use to manage the framerate of the game

# Main game loop
while True:

	for event in pygame.event.get(): # Check for pygame events (keypress, close window, etc.)
		if event.type == pygame.QUIT:
			sys.exit() # Close the program if the user sends a QUIT signal (closes the window)

		if event.type == pygame.KEYDOWN: # If the user presses down a key
			if event.key == pygame.K_ESCAPE:
				sys.exit() # Quit the program if the user presses ESCAPE

		if event.type == pygame.KEYUP: # If the user releases a key
			if event.key in (pygame.K_UP, pygame.K_DOWN):
				bar2.move(0) # Once the right player releases their movement keys, set bar2's speed to 0

			if event.key in (pygame.K_w, pygame.K_s):
				bar1.move(0) # Once the left player releases their movement keys, set bar1's speed to 0

	keys = pygame.key.get_pressed() # Check all of the keys that are currently being pressed down
	if keys[pygame.K_UP]: # Move bar2, if the right player is holding down one of their movement keys
		bar2.move(-1*BAR_SPEED)
	elif keys[pygame.K_DOWN]:
		bar2.move(BAR_SPEED)

	if keys[pygame.K_w]: # Move bar1, if the left player is holding down one of their movement keys
		bar1.move(-1*BAR_SPEED)
	elif keys[pygame.K_s]:
		bar1.move(BAR_SPEED)

	# Check if the ball hits either of the bars, if so reverse it's x direction
	if (ball.x - BALL_SIZE/2)  - bar1.x >= 0 and (ball.x - BALL_SIZE/2)  - bar1.x <= 7 and abs(ball.y - bar1.y) < (BAR_LENGTH+BALL_SIZE)/2:
		ball.move(new_xspeed = -1*ball.xspeed)
	elif bar2.x - (ball.x + BALL_SIZE/2) >= 0 and bar2.x - (ball.x + BALL_SIZE/2)  <= 7 and abs(ball.y - bar2.y) < (BAR_LENGTH+BALL_SIZE)/2:
		ball.move(new_xspeed = -1*ball.xspeed)

	ball.move() # Move the ball

	window.blit(background,(0,0)) # Blit the background to the screen with top left corner aligned at (0,0)
	window.blit(bar1.surface,(bar1.x - 5,bar1.y-BAR_LENGTH/2)) # Blit bar one, using the midpoint to determine where its top left corner is
	window.blit(bar2.surface,(bar2.x - 5,bar2.y-BAR_LENGTH/2)) # Blit bar two in the same way
	window.blit(ball.surface,(ball.x - BALL_SIZE/2, ball.y - BALL_SIZE/2))

	clock.tick(FPS) # Use this command to make sure the game loop runs no more than FPS times per second
	pygame.display.update() # Update the pygame window
