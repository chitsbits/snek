#########################################
# Filename: Snek.py
# Description: Snek game
# Author: Sunny Jiao
# Date: 11/07/18
#########################################

from random import randint
import time
import pygame

# Used to fix delayed sounds
pygame.mixer.pre_init(44100,-16,1, 2048)

pygame.init()

# Game Dimensions               ## Resolution is scalable when dimensions are increased by increments of 20 pixels ##
WIDTH = 1200
HEIGHT= 900
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

# Colours
GREY = (150,150,150)
GREY2 = ( 70, 70, 70)
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
GREEN = (  0,255,  0)
RED = (255,  0,  0)
YELLOW = (255,255,  0)
BROWN = (202,132,  0)
DARK_PURPLE = ( 21, 5, 24)
PURPLE = (175, 85,255)
CYAN = ( 85,247,255)
ORANGE = (255,104, 13)
outline = 0

# Load fonts, images and sounds
font1 = pygame.font.SysFont("Courier New",40)
font2 = pygame.font.SysFont("Courier New",20)

title = pygame.image.load("snektitle.png").convert_alpha()
snek = pygame.image.load("snek.png").convert_alpha()
snekDed = pygame.image.load("snek_ded.png").convert_alpha()

pygame.mixer.music.load("snekost.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

death = pygame.mixer.Sound("death.wav")
death.set_volume(0.2)
eat = pygame.mixer.Sound("nom.wav")
eat.set_volume(0.2)
speedUp = pygame.mixer.Sound("speedup.wav")
speedUp.set_volume(0.2)
buttonSound = pygame.mixer.Sound("button.wav")
buttonSound.set_volume(0.2)

#---------------------------------------#
# Functions                             #
#---------------------------------------#

def redrawGameWindow():                  # Draw main game screen
    gameWindow.fill(GREY)

    # Draw information bar
    pygame.draw.rect(gameWindow, DARK_PURPLE, (SEGMENT_R,90, WIDTH - 2*SEGMENT_R, HEIGHT - 2*SEGMENT_R - 80),outline)
    pygame.draw.rect(gameWindow, GREY2, (SEGMENT_R,SEGMENT_R, WIDTH-2*SEGMENT_R, 70),outline)
    scoreText = font1.render("Score: "+str(score),1,WHITE)
    gameWindow.blit(scoreText,(20,20))

    if timeEnabled:
        secondZero = ""
        if secondsLeft < 10:
            secondZero = "0"
        countdown = font1.render("Time: "+str(minutesLeft)+":"+secondZero+str(secondsLeft),1,WHITE)
        gameWindow.blit(countdown,(WIDTH - countdown.get_width() - 20,20))

    if score == 10 or score == 20 or score == 30:
        speedUp = font2.render("SPEED INCREASED",1,WHITE)
        gameWindow.blit(speedUp,(scoreText.get_width() + 50, 25))

    # Draw snake
    for i in range(len(segX)):
        if i % 4 == 0:
            pygame.draw.circle(gameWindow, secondSegColour, (segX[i], segY[i]), SEGMENT_R, outline)       # Secondary segment colour
        else:
            pygame.draw.circle(gameWindow, mainSegColour, (segX[i], segY[i]), SEGMENT_R, outline)         # Primary segment colour
    pygame.draw.rect(gameWindow, headCLR, (segX[0]-SEGMENT_R, segY[0]-SEGMENT_R, 2*SEGMENT_R, 2*SEGMENT_R), outline) # Head

    # Draw obstacles
    for i in range(len(obstacleXList)): 
        pygame.draw.rect(gameWindow, YELLOW, (obstacleXList[i] - SEGMENT_R, obstacleYList[i] - SEGMENT_R, 2*SEGMENT_R, 2*SEGMENT_R),outline)
    # Draw apples
    for i in range(len(appleXList)):
        pygame.draw.circle(gameWindow,RED, (appleXList[i],appleYList[i]),SEGMENT_R,outline)

def generateApple():                    # Generate Coordinates for apple
    appleX = randint(1,(WIDTH - 2*SEGMENT_R)/HSTEP)*HSTEP
    appleY = randint(5,(HEIGHT - 2*SEGMENT_R)/HSTEP)*HSTEP

    # Loop to ensure apple does not spawn inside snake or on an obstacle
    goodApple = False
    while goodApple == False:
        goodApple = True

        # Iterate through segments to check if apple is intersecting with snake/obstacle
        # If intersection is detected, generate a new apple and restart the check
        for i in range(len(segX)):
            if appleX == segX[i] and appleY == segY[i]:
                appleX = randint(1,(WIDTH - 2*SEGMENT_R)/HSTEP)*HSTEP
                appleY = randint(5,(HEIGHT - 2*SEGMENT_R)/HSTEP)*HSTEP
                goodApple = False

        # Same thing, but for obstacles
        for i in range(len(obstacleXList)):
            if appleX == obstacleXList[i] and appleY == obstacleYList[i]:
                appleX = randint(1,(WIDTH - 2*SEGMENT_R)/HSTEP)*HSTEP
                appleY = randint(5,(HEIGHT - 2*SEGMENT_R)/HSTEP)*HSTEP
                goodApple = False
            
    appleXList.append(appleX)
    appleYList.append(appleY)

def generateObstacles():                # Generate coordinates for obstacles
    # Generate 3 - 7 obstacles
    for i in range(randint(3,7)):
        obstacleX = randint(1,(WIDTH - 2*SEGMENT_R)/HSTEP)*HSTEP
        obstacleY = randint(5,(HEIGHT - 2*SEGMENT_R)/HSTEP)*HSTEP
        obstacleXList.append(obstacleX)
        obstacleYList.append(obstacleY)

def redrawMainMenu():                   # Draw main menu screen
    gameWindow.fill(BLACK)
    gameWindow.blit(title,(WIDTH/2 - title.get_width()/2,0))
    pressEnter = font1.render("PRESS ENTER TO START",1,WHITE)
    customizePrompt = font2.render("Customize Snake:",1,WHITE)
    primaryPrompt = font2.render("Primary:",1,WHITE)
    secondaryPrompt = font2.render("Secondary:",1,WHITE)
    gameWindow.blit(customizePrompt,(WIDTH/2 - customizePrompt.get_width()/2,HEIGHT/2 + 30))
    gameWindow.blit(primaryPrompt,(WIDTH/2 - 150 - primaryPrompt.get_width()/2,HEIGHT/2 + 50))
    gameWindow.blit(secondaryPrompt,(WIDTH/2 + 150 - primaryPrompt.get_width()/2,HEIGHT/2 + 50))
    gameWindow.blit(snek,(WIDTH/2 - snek.get_width()/2 - 20,HEIGHT/4))

    # Flashing "PRESS ENTER" message
    if blinkOn == True:
        gameWindow.blit(pressEnter,(WIDTH/2 - pressEnter.get_width()/2,HEIGHT - 80))

    # Option Buttons
    obstaclesPrompt = font2.render("Obstacles",1,WHITE) # Obstacles
    musicPrompt = font2.render("Music",1,WHITE)         # Music
    timePrompt = font2.render("Time Limit",1,WHITE)     # Time Limit
    pygame.draw.rect(gameWindow, obstacleButton,(WIDTH/2 - 220, HEIGHT/2 - SEGMENT_R,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, musicButton,(WIDTH/2 - 30, HEIGHT/2 - SEGMENT_R,2*SEGMENT_R,2*SEGMENT_R),outline)          
    pygame.draw.rect(gameWindow, timeButton,(WIDTH/2 + 100, HEIGHT/2 - SEGMENT_R, 2*SEGMENT_R, 2*SEGMENT_R),outline)
    gameWindow.blit(obstaclesPrompt,(WIDTH/2 - 190,HEIGHT/2 - obstaclesPrompt.get_height()/2))
    gameWindow.blit(musicPrompt,(WIDTH/2,HEIGHT/2 - musicPrompt.get_height()/2))
    gameWindow.blit(timePrompt,(WIDTH/2 + 130,HEIGHT/2 - timePrompt.get_height()/2))

    # Snake Customization
    pygame.draw.rect(gameWindow, GREEN,(WIDTH/2 - 220, HEIGHT/2 + 90,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, PURPLE,(WIDTH/2 - 220, HEIGHT/2 + 130,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, BROWN,(WIDTH/2 - 220, HEIGHT/2 + 170,2*SEGMENT_R,2*SEGMENT_R),outline)

    pygame.draw.rect(gameWindow, WHITE,(WIDTH/2 - 180, HEIGHT/2 + 90,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, CYAN,(WIDTH/2 - 180, HEIGHT/2 + 130,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, ORANGE,(WIDTH/2 - 180, HEIGHT/2 + 170,2*SEGMENT_R,2*SEGMENT_R),outline)

    pygame.draw.rect(gameWindow, GREEN,(WIDTH/2 + 220, HEIGHT/2 + 90,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, PURPLE,(WIDTH/2 + 220, HEIGHT/2 + 130,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, BROWN,(WIDTH/2 + 220, HEIGHT/2 + 170,2*SEGMENT_R,2*SEGMENT_R),outline)

    pygame.draw.rect(gameWindow, WHITE,(WIDTH/2 + 180, HEIGHT/2 + 90,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, CYAN,(WIDTH/2 + 180, HEIGHT/2 + 130,2*SEGMENT_R,2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, ORANGE,(WIDTH/2 + 180, HEIGHT/2 + 170,2*SEGMENT_R,2*SEGMENT_R),outline)

    pygame.draw.rect(gameWindow, mainSegColour,(WIDTH/2 - 40, HEIGHT/2 + 130, 2*SEGMENT_R, 2*SEGMENT_R),outline)
    pygame.draw.rect(gameWindow, secondSegColour,(WIDTH/2 + 40, HEIGHT/2 + 130, 2*SEGMENT_R, 2*SEGMENT_R),outline)
    
def redrawGameOverScreen(): # Draw game over screen
    gameWindow.fill(BLACK)
    gameOver = font1.render("GAME OVER",1,WHITE)
    gameWindow.blit(gameOver,(WIDTH/2 - gameOver.get_width()/2,HEIGHT/2 - gameOver.get_height()/2))
    scoreText = font1.render("Score: "+str(score),1,WHITE)
    gameWindow.blit(scoreText,(WIDTH/2 - scoreText.get_width()/2, HEIGHT/2 + 20))
    escapePrompt = font1.render("Press ESC to exit",1,WHITE)
    gameWindow.blit(escapePrompt,(WIDTH/2 - escapePrompt.get_width()/2, HEIGHT - 50))
    gameWindow.blit(snekDed,(WIDTH/2 - snekDed.get_width()/2 - 20, HEIGHT/7))
    pygame.display.update()

#---------------------------------------#
# Main program                          #
#---------------------------------------#

# Game Properties

# Player
score = 0

# Snake
mainSegColour = GREEN
secondSegColour = BROWN
headCLR = WHITE
SEGMENT_R = 10                          # Game can be scaled as long as HSTEP and VSTEP are 2x SEGMENT_R
HSTEP = 20
VSTEP = 20
stepX = 0
stepY = -VSTEP                          # Initially the snake moves upwards
segX = []
segY = []
segIncrease = 2                         # Number of segments each apple adds

# Apples
appleXList = []
appleYList = []
segIncrease = 2                 
APPLE_INTERVAL = 2                      # Time in seconds between apple spawns

# Obstacles
obstacleXList = []
obstacleYList = []

# Main Menu
obstacleButton = GREEN
obstaclesEnabled = True                
musicButton = GREEN
musicEnabled = True
timeButton = GREEN
timeEnabled = True
blinkOn = True

# Time
clock = pygame.time.Clock()
fps = 18
elapsed = 0
timeLimit = 150                         # Time limit in seconds
minutesLeft = 0
secondsLeft = 0

#---------------------------------------------#
################## Menu Loop ##################
#---------------------------------------------#

MENU_BEGIN = time.time()
referenceTime = MENU_BEGIN

inMenu = True
while inMenu:
    redrawMainMenu()      
    pygame.display.update()

    # Make "Press enter to start" blink on and off
    menuElapsed = time.time() - referenceTime
    if round(menuElapsed,3) >= 0.525:
        referenceTime = time.time()
        if blinkOn == True:
            blinkOn = False
        else:
            blinkOn = True

    mousePos = pygame.mouse.get_pos()                # Use mouse input to adjust game settings
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Enable obstacles
            if mousePos[0] > WIDTH/2 - 220 and mousePos[0] < WIDTH/2 - 200 + 2*SEGMENT_R and mousePos[1] < HEIGHT/2 + SEGMENT_R and mousePos[1] > HEIGHT/2 - SEGMENT_R:
                if obstaclesEnabled == False:
                    obstaclesEnabled = True
                    obstacleButton = GREEN
                else:
                    obstaclesEnabled = False
                    obstacleButton = RED
                buttonSound.play(0)

            # Enable Music
            if mousePos[0] > WIDTH/2 - 30 and mousePos[0] < WIDTH/2 - 30 + 2*SEGMENT_R and mousePos[1] < HEIGHT/2 + SEGMENT_R and mousePos[1] > HEIGHT/2 - SEGMENT_R:
                if musicEnabled == False:
                    musicEnabled = True
                    musicButton = GREEN
                else:
                    musicEnabled = False
                    musicButton = RED
                buttonSound.play(0)

            # Enable Timer
            if mousePos[0] > WIDTH/2 + 100 and mousePos[0] < WIDTH/2 + 100 + 2*SEGMENT_R and mousePos[1] < HEIGHT/2 + SEGMENT_R and mousePos[1] > HEIGHT/2 - SEGMENT_R:
                if timeEnabled == False:
                    timeEnabled = True
                    timeButton = GREEN
                else:
                    timeEnabled = False
                    timeButton = RED
                buttonSound.play(0)

            # Customization buttons
            # Primary segment colours
            if mousePos[0] > WIDTH/2 - 220 and mousePos[0] < WIDTH/2 - 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 90 and mousePos[1] < HEIGHT/2 + 90 + 2*SEGMENT_R:
                mainSegColour = GREEN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 - 220 and mousePos[0] < WIDTH/2 - 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 130 and mousePos[1] < HEIGHT/2 + 130 + 2*SEGMENT_R:
                mainSegColour = PURPLE
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 - 220 and mousePos[0] < WIDTH/2 - 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 170 and mousePos[1] < HEIGHT/2 + 170 + 2*SEGMENT_R:
                mainSegColour = BROWN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 - 180 and mousePos[0] < WIDTH/2 - 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 90 and mousePos[1] < HEIGHT/2 + 90 + 2*SEGMENT_R:
                mainSegColour = WHITE
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 - 180 and mousePos[0] < WIDTH/2 - 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 130 and mousePos[1] < HEIGHT/2 + 130 + 2*SEGMENT_R:
                mainSegColour = CYAN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 - 180 and mousePos[0] < WIDTH/2 - 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 170 and mousePos[1] < HEIGHT/2 + 170 + 2*SEGMENT_R:
                mainSegColour = ORANGE
                buttonSound.play(0)

            # Secondary segment colours
            if mousePos[0] > WIDTH/2 + 220 and mousePos[0] < WIDTH/2 + 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 90 and mousePos[1] < HEIGHT/2 + 90 + 2*SEGMENT_R:
                secondSegColour = GREEN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 + 220 and mousePos[0] < WIDTH/2 + 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 130 and mousePos[1] < HEIGHT/2 + 130 + 2*SEGMENT_R:
                secondSegColour = PURPLE
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 + 220 and mousePos[0] < WIDTH/2 + 220 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 170 and mousePos[1] < HEIGHT/2 + 170 + 2*SEGMENT_R:
                secondSegColour = BROWN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 + 180 and mousePos[0] < WIDTH/2 + 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 90 and mousePos[1] < HEIGHT/2 + 90 + 2*SEGMENT_R:
                secondSegColour = WHITE
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 + 180 and mousePos[0] < WIDTH/2 + 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 130 and mousePos[1] < HEIGHT/2 + 130 + 2*SEGMENT_R:
                secondSegColour = CYAN
                buttonSound.play(0)
            if mousePos[0] > WIDTH/2 + 180 and mousePos[0] < WIDTH/2 + 180 + 2*SEGMENT_R and mousePos[1] > HEIGHT/2 + 170 and mousePos[1] < HEIGHT/2 + 170 + 2*SEGMENT_R:
                secondSegColour = ORANGE
                buttonSound.play(0)

    # Enable / Disable music
    if musicEnabled == False:
        pygame.mixer.music.set_volume(0.0)
    if musicEnabled == True:
        pygame.mixer.music.set_volume(0.2)
            
    pygame.event.clear()
    keys = pygame.key.get_pressed()         # Main menu will display until user presses ESC or ENTER
    if keys[pygame.K_RETURN]:
        inMenu = False
    elif keys[pygame.K_ESCAPE]:
        pygame.quit()

#----------------------------------------------#
##################  Pre-game  ##################
#----------------------------------------------#

for i in range(6):                          # Add beginning coordinates for the head and 3 segments
    segX.append(WIDTH / 2)
    segY.append(HEIGHT + i*VSTEP)

GAME_BEGIN = time.time()                    # Start timer
referenceTime = GAME_BEGIN
        
if obstaclesEnabled:
    generateObstacles()                     # Generate obstacles, if enabled by user

generateApple()                             # Generate first apple

#----------------------------------------------#
##################  Game Loop ##################
#----------------------------------------------#
                                     
inPlay = True
while inPlay:

# Move the segments
    lastIndex = len(segX)-1
    for i in range(lastIndex,0,-1):         # starting from the tail, and going backwards:
        segX[i]=segX[i-1]                   # every segment takes the coordinates
        segY[i]=segY[i-1]                   # of the previous one
        
# Move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY
    
# Check if snake has hit border
    if segX[0] <= 0 or segX[0] >= WIDTH or segY[0] <= 90 or segY[0] >= HEIGHT:
        inPlay = False
        
# Check if snake has cut itself
    for i in range(lastIndex,0,-1):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            inPlay = False

# Check if snake has hit obstacle
    for i in range(len(obstacleXList)):
        if segX[0] == obstacleXList[i] and segY[0] == obstacleYList[i]:
            inPlay = False
    
# Check if snake has eaten an apple
    for i in range(len(appleXList)):

        # Stop checking once an apple is popped.
        # this if statement prevents the check from happening if the index is out of range
        if i < len(appleXList):

            # Iterate through apples, pop apple if intersecting with head
            if segX[0] == appleXList[i] and segY[0] == appleYList[i]:
                for j in range(segIncrease):
                    segX.append(segX[-1])                            # Add segment: append new segment with the same x and y coordinates
                    segY.append(segY[-1])                            # as the previous segment
                appleXList.pop(i)                                    # Remove apple from list
                appleYList.pop(i)
                score += 1
                eat.play(0)
                
                if score == 10 or score == 20 or score == 30:        # Increase speed at 10, 20, 30 score
                    fps += 1
                    speedUp.play(0)

# Apple spawn timer
    appleElapsed = round(time.time() - referenceTime, 1)
    if appleElapsed > APPLE_INTERVAL:
        generateApple()
        referenceTime = time.time()

# Game Timer
    if timeEnabled == True:
        elapsed = int(time.time() - GAME_BEGIN)
        timeLeft = timeLimit - elapsed
        minutesLeft = timeLeft / 60
        secondsLeft = timeLeft % 60

        if elapsed == timeLimit:
            inPlay = False

# Inputs
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    elif keys[pygame.K_LEFT]:
        if stepX != HSTEP:
                stepX = -HSTEP
                stepY = 0
    elif keys[pygame.K_RIGHT]:
            if stepX != -HSTEP:
                stepX = HSTEP
                stepY = 0
    elif keys[pygame.K_UP]:
            if stepY != VSTEP:
                stepX = 0
                stepY = -VSTEP
    elif keys[pygame.K_DOWN]:
            if stepY != -VSTEP:
                stepX = 0
                stepY = VSTEP

    if inPlay:
        redrawGameWindow()
        pygame.display.update()
    clock.tick(fps)

#---------------------------------------------------#
##################  Game Over Loop ##################
#---------------------------------------------------#
pygame.mixer.music.set_volume(0)
death.play(0)

gameOver = True
while gameOver:
    redrawGameOverScreen()

    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        gameOver = False

pygame.quit()
