# Pong

import random, sys, pygame, math
from pygame.locals import *

# Design parameters
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BACKGROUNDCOLOR = BLACK
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
MARGIN = 50
TEXTCOLOR = WHITE
SCOREWIDTH = 30
SCOREHEIGHT = 60
SCORELINEWIDTH = 10

# Gameplay paramters
FPS = 60
PLAYERSPEED = 20
BALLSPEED = 7
BALLSIZE = 5

# Functions and classes definitions
def waitForPlayerToContinue():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN or event.key == K_SPACE:
                    return


def drawText(text, font, surface, x, y):
    ''' Display text on the surface '''
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

    
def terminate():
    pygame.quit()
    sys.exit()


def norm1(vector):
    ''' Compute the norm1 of a vector (list)'''
    norm = 0
    for x in vector:
        norm += abs(x)
    return norm


def normalize(vector):
    ''' Normalize with norm1 a vector (list)'''
    norm = norm1(vector)
    for i in range(len(vector)):
        vector[i] /= norm
    return vector


def drawNet(windowSurface):
    width = 5
    height = 7
    space = 7
    y = 0
    while y < WINDOWHEIGHT:
        pygame.draw.rect(windowSurface, WHITE, pygame.Rect( (WINDOWWIDTH - width)/2, y, width, height))
        y += height + space                                                    


def displayScore(score1, score2):
    ''' Display the score on the screen (player1 and player2)'''
    if score1 < 10:
        score1 = '0' + str(score1)
    else:
        score1 = str(score1)
    if score2 < 10:
        score2 = '0' + str(score2)
    else:
        score2 = str(score2)
    # score player 1
    draw_0_9(WINDOWWIDTH/2 - 50 - (SCOREWIDTH + 10), 10, score1[0])
    draw_0_9(WINDOWWIDTH/2 - 50, 10, score1[1]) 
    # score player 2
    draw_0_9(WINDOWWIDTH/2 + 50 - SCOREWIDTH, 10, score2[0]) 
    draw_0_9(WINDOWWIDTH/2 + 50 + 10, 10, score2[1])


def draw_0_9(left, top, n):
    if n == '0':
        pattern = (1, 1, 1, 1,
                   1, 0, 0, 1,
                   1, 0, 0, 1,
                   1, 0, 0, 1,
                   1, 1, 1, 1)
    elif n == '1':
        pattern = (0, 1, 1, 0,
                   0, 0, 1, 0,
                   0, 0, 1, 0,
                   0, 0, 1, 0,
                   0, 1, 1, 1)
    elif n == '2':
        pattern = (1, 1, 1, 1,
                   0, 0, 1, 1,
                   1, 1, 1, 1,
                   1, 1, 0, 0,
                   1, 1, 1, 1)
    elif n == '3':
        pattern = (1, 1, 1, 1,
                   0, 0, 1, 1,
                   1, 1, 1, 1,
                   0, 0, 1, 1,
                   1, 1, 1, 1)
    elif n == '4':
        pattern = (1, 0, 0, 0,
                   1, 0, 0, 1,
                   1, 1, 1, 1,
                   0, 0, 0, 1,
                   0, 0, 0, 1)
    elif n == '5':
        pattern = (1, 1, 1, 1,
                   1, 1, 0, 0,
                   1, 1, 1, 1,
                   0, 0, 1, 1,
                   1, 1, 1, 1)
    elif n == '6':
        pattern = (1, 1, 1, 1,
                   1, 1, 0, 0,
                   1, 1, 1, 1,
                   1, 1, 0, 1,
                   1, 1, 1, 1)
    elif n == '7':
        pattern = (1, 1, 1, 1,
                   1, 0, 1, 1,
                   0, 0, 1, 1,
                   0, 0, 1, 1,
                   0, 0, 1, 1)
    elif n == '8':
        pattern = (1, 1, 1, 1,
                   1, 0, 0, 1,
                   1, 1, 1, 1,
                   1, 0, 0, 1,
                   1, 1, 1, 1)
    elif n == '9':
        pattern = (1, 1, 1, 1,
                   1, 0, 1, 1,
                   1, 1, 1, 1,
                   0, 0, 1, 1,
                   0, 0, 1, 1)
        
    for i in range(len(pattern)):
        if pattern[i] == 1:
            pygame.draw.rect(windowSurface, WHITE,
                         pygame.Rect(left + i%4 * math.floor(SCOREWIDTH/4),
                                     top + i//4 * math.floor(SCOREHEIGHT/5),
                                     math.floor(SCOREWIDTH/4),
                                     math.floor(SCOREHEIGHT/5)))


def drawStartMenu():
    drawText('Welcome to pong!', font, windowSurface, WINDOWWIDTH/2- 125, WINDOWHEIGHT/2 - 35)
    drawText('Press enter to start.', font, windowSurface, WINDOWWIDTH/2 - 125, WINDOWHEIGHT/2 + 35)

    
class Player():
    '''Class for the player'''
    width = 10
    height = 50
    def __init__(self,pos):
        if pos == 1:
            x_start = MARGIN
        elif pos == 2:
            x_start = WINDOWWIDTH - MARGIN
        y_start = (WINDOWHEIGHT  - self.height) / 2
        self.rect = pygame.Rect(x_start, y_start, self.width, self.height)
        self.dir = 0;
        self.score = 0
        
    def move(self):
        newY = self.rect.top + self.dir * PLAYERSPEED
        if newY < 0 : # ne doit pas dépasser du terrain
            newY = 0
        if newY > WINDOWWIDTH - self.height:
            newY = WINDOWWIDTH -  self.height
        # update rect position
        self.rect.top = newY


class Ball():
    ''' Class for the ball '''
    def __init__(self, whoServes):
        self.hasCollided = False
        self.dir = [0, 0]
        self.speed = BALLSPEED
        self.rect = pygame.Rect((WINDOWWIDTH - BALLSIZE)/2,
                                random.randint(20, WINDOWHEIGHT - 20),
                                BALLSIZE, BALLSIZE)
        # initial angle
        if whoServes == 1: # player1 (left) serves
            self.dir[0] = random.randint(5,10)
        elif whoServes == 2: # player2 (right) serves
            self.dir[0] = - random.randint(5,10)
        self.dir[1] = random.randint(-5,5) 
        self.dir = normalize(self.dir)

    def isOut(self):
        ''' Return the number of the player who scored, or false'''
        if self.rect.left < 0:
            return 2
        elif self.rect.right > WINDOWWIDTH:
            return 1
        else:
            return False
        
    def hitByPlayer(self, player):
        ''' set the new direction and speed after bouncing the player'''
        self.dir[0] = -self.dir[0]
        dy = (player.rect.centery - self.rect.centery) / (player.height)
        self.dir[1] -= dy
        self.dir = normalize(self.dir)
        self.speed +=  abs(dy)
        # set a maximum angle for y
        if self.dir[1] > 0.5:
            self.dir[1] = 0.5
            self.dir = normalize(self.dir)
        if self.dir[1] < -0.5:
            self.dir[1] = -0.5
            self.dir = normalize(self.dir)    

    def update(self):
        ''' update the position and the new direction of the ball'''
        # update position
        self.rect.left += self.speed * self.dir[0]
        self.rect.top += self.speed * self.dir[1]
        # update direction
        if self.rect.colliderect(player1.rect):
            self.rect.left = player1.rect.right
            self.hitByPlayer(player1)
        elif self.rect.colliderect(player2.rect):
            self.rect.right = player2.rect.left
            self.hitByPlayer(player2)
        elif self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
            self.dir[1] = - self.dir[1]
        elif self.rect.top < 0:
            self.rect.top = 0
            self.dir[1] = - self.dir[1]
   
              
# Initialisation
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Pong')

# set up fonts
font = pygame.font.SysFont(None, 40)

# Start Menu
drawStartMenu()
pygame.display.update()
waitForPlayerToContinue()

# Game objects creation
whoServes = random.randint(1,2)
player1 = Player(1)
player2 = Player(2)
ball = Ball(whoServes)

# Game loop
while True:

    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            if event.key == ord('w') and player1.dir == -1:
                player1.dir = 0
            if event.key == ord('s') and player1.dir == 1:
                player1.dir = 0
            if event.key == K_UP and player2.dir == -1:
                player2.dir = 0
            if event.key == K_DOWN and player2.dir == 1:
                player2.dir = 0
        if event.type == KEYDOWN:
            if event.key == ord('w'):
                player1.dir = -1
            if event.key == ord('s'):
                player1.dir = 1                
            if event.key == K_UP:
                player2.dir = -1
            if event.key == K_DOWN:
                player2.dir = 1  

    # update players position and ball
    ball.update()
    player1.move()
    player2.move()
    
    # drawing
    windowSurface.fill(BACKGROUNDCOLOR)
    drawNet(windowSurface)
    pygame.draw.rect(windowSurface, WHITE, player1.rect)
    pygame.draw.rect(windowSurface, WHITE, player2.rect)

    # if the ball is outside
    isOut = ball.isOut()
    if isOut:
        if isOut == 1:
            player1.score += 1
        elif isOut == 2:
            player2.score += 1
        del(ball)
        whoServes = isOut
        displayScore(player1.score, player2.score)
        
        # Victory conditions
        if player1.score == 11 or player2.score == 11:
            drawText('Player %s Won!' %(isOut), font, windowSurface, WINDOWWIDTH/2- 75, WINDOWHEIGHT/2 - 35)
            drawText('Press enter to restart or escape to quit.', font, windowSurface, WINDOWWIDTH/2 - 250, WINDOWHEIGHT/2 + 35)
            pygame.display.update()
            waitForPlayerToContinue()
            # init game
            whoServes = 1
            player1 = Player(1)
            player2 = Player(2)
            ball = Ball(whoServes)
            continue
            
        pygame.display.update()
        waitForPlayerToContinue()
        # if we press to enter, reset the ball and player's movement
        ball = Ball(whoServes)
        player1.dir = 0
        player2.dir = 0
        
    # ball drawing
    pygame.draw.rect(windowSurface, WHITE, ball.rect)
    displayScore(player1.score, player2.score)
    # update display
    pygame.display.update()
    # update the clock
    mainClock.tick(FPS)
    
