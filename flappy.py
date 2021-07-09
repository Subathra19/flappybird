from typing import Mapping
import pygame
import random
# To exit the code using sys.exit
import sys

from pygame import transform
from pygame.constants import KEYDOWN, K_UP

###########################################
#  Global variables
###########################################

# number of frames changing per second
fps=32
screen_width=280
screen_height=570

base_x=0
base_y=screen_height * 0.8

# Create a Screen
screen=pygame.display.set_mode((screen_width,screen_height))

# Images to be added on screen
game_images={}

# sounds to be used on game
game_sounds={}

# Add location of images
flappy='images/bluebird.png'
background='images/background-day.png'
pipe='images/pipe.png'


###########################################
#  Functions
###########################################

def welcome_screen():
    flappy_x=int(screen_width/4)
    flappy_y=int(screen_height/1.7)

    # Place the message in center 
    message_x=int((screen_width-game_images["message"].get_width())/2)
    message_y=int((screen_height-game_images["message"].get_height())/2)


    while True:
        for event in pygame.event.get():
            # If a player clicks on QUIT(X) 
            if event.type== pygame.QUIT or (event.type==KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Returns to gaming screen
            elif event.type==KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                return
            else:
                # Blit->pasting the images on screen
                screen.blit(game_images['background'],(0,0))
                screen.blit(game_images['flappy'],(flappy_x,flappy_y))
                screen.blit(game_images['message'],(message_x,message_y))
                screen.blit(game_images['base'],(base_x,base_y))

                pygame.display.update()
                fps_clock.tick(fps)


def get_random_pipe():
    # As we have two pipes
    pipe_height=game_images['pipe'][0].get_height()
    offset=screen_height/3
    
    # Position of pipes ---> Distance between pipes
    rand_x=screen_width+10
    # position of lower pipe
    rand_y2=offset+random.randrange(0,int(screen_height-game_images['base'].get_height()-1.2*offset))
    # position of upper pipe
    rand_y1=pipe_height-rand_y2+offset
    # Position of upper and lower pipe 
    pipe=[
        {"x": rand_x, "y": -rand_y1},
        {"x": rand_x, "y": rand_y2}
    ]
    return pipe


def check_collision(flappy_x,flappy_y,lower_pipes,upper_pipes):
    # If flappy hits the ground or hits the top
    if flappy_y > base_y-25 or flappy_y <0:
        game_sounds["hit"].play()
        return True
    
    
    # If flappy hits the lower pipe
    for pipe in lower_pipes:
        if(flappy_y+game_images["flappy"].get_height()>pipe["y"]) and abs(flappy_x - pipe["x"]) < game_images["pipe"][0].get_width():
            game_sounds["hit"].play()
            return True
    
    # If flappy hits the upper pipe
    for pipe in upper_pipes:
        pipe_height=game_images["pipe"][0].get_height()
        if(flappy_y<pipe_height+pipe["y"]) and abs(flappy_x - pipe["x"]) < game_images["pipe"][0].get_width():
            game_sounds["hit"].play()
            return True

    return False


# Main game                
def game_screen():
    # Initialize score
    score=0
    flappy_x=screen_width/5
    flappy_y=screen_height/2

    # Create a list of new pipes
    new_pipe1=get_random_pipe()
    new_pipe2=get_random_pipe()

    upper_pipes=[
        {"x": screen_width+200, "y":new_pipe1[0]["y"]},
        {"x": screen_width+200+(screen_width/2), "y":new_pipe2[0]["y"]}
    ]

    lower_pipes=[
        {"x": screen_width+200, "y":new_pipe1[1]["y"]},
        {"x": screen_width+200+(screen_width/2), "y":new_pipe2[1]["y"]}
    ]

    # Pipe moving in -x direction
    pipe_velocity_x=-4

    flappy_velocity_y=-9
    flappy_velocity_y_max=10
    flappy_velocity_y_min=-8
    flappy_acceleration_y=1

    flapping_velocity=-8

    flapped=False

    while True:
        for event in pygame.event.get():
            # If a player clicks on QUIT(X) 
            if event.type==pygame.QUIT or (event.type==KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                if flappy_y>0:
                    flappy_velocity_y=flapping_velocity
                    flapped=True
                    game_sounds["wing"].play()
        
        # To check whether flappy hits the pipes or not
        crash=check_collision(flappy_x,flappy_y,lower_pipes,upper_pipes)

        if crash: 
            return
        
        # Update the scores
        flappy_middle_position=flappy_x+game_images["flappy"].get_width()/2 
        for pipe in upper_pipes:
            pipe_middle_position=pipe["x"]+game_images["pipe"][0].get_width()/2 
            if pipe_middle_position <= flappy_middle_position <pipe_middle_position+4:
                score=score+1
                game_sounds["points"].play()

        # Movement of flappy
        if flappy_velocity_y<flappy_velocity_y_max and not flapped:
            flappy_velocity_y=flappy_velocity_y+flappy_acceleration_y
        
        if flapped:
            flapped=False
        
        flappy_height=game_images["flappy"].get_height()
        # Change the position of flappy
        flappy_y=flappy_y+ min(flappy_velocity_y, base_y-flappy_y-flappy_height)
        
        # Move pipes to the left
        for lower,upper in zip(lower_pipes,upper_pipes):
            lower["x"]=lower["x"]+pipe_velocity_x
            upper["x"]=upper["x"]+pipe_velocity_x
        
        # Add a new pipe when the left most pipe is almost out of screen
        if upper_pipes[0]["x"]>0 and upper_pipes[0]["x"]<5:
            newpipe=get_random_pipe()
            lower_pipes.append(newpipe[1])
            upper_pipes.append(newpipe[0])

        # Remove the pipe which is going out of screen
        if upper_pipes[0]["x"] < -game_images["pipe"][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
        
        # Blit images on screen
        screen.blit(game_images["background"],(0,0))

        for lower,upper in zip(lower_pipes,upper_pipes):
            screen.blit(game_images["pipe"][1],(lower["x"],lower["y"]))
            screen.blit(game_images["pipe"][0],(upper["x"],upper["y"]))

        screen.blit(game_images["base"],(base_x,base_y))
        screen.blit(game_images["flappy"],(flappy_x,flappy_y))

        score_list=[int(x) for x in list(str(score))]
        score_width=0
        
        for i in score_list:
            score_width=score_width+game_images["numbers"][i].get_width()

        offset_x= (screen_width-score_width)/2
        
        for i in score_list:
            screen.blit(game_images["numbers"][i],(offset_x,screen_height*0.12))
            offset_x=offset_x+game_images["numbers"][i].get_width()

        pygame.display.update()
        fps_clock.tick(fps)


###########################################
# Main function from where game starts
###########################################
if __name__=="__main__":
    # Intilialize all pygame modules
    pygame.init()    
    fps_clock=pygame.time.Clock()
    pygame.display.set_caption("Flappy bird")
    
    # To display scores on screen
    # For faster blending of image on screen convert_alpha() is used [Optimization]
    game_images["numbers"]=(
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images["message"]=pygame.image.load('images/message.png').convert_alpha()
    game_images["base"]=pygame.image.load('images/base.png').convert_alpha()
    
    game_images["pipe"]=(
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
        pygame.image.load(pipe).convert_alpha()
    )

    # As background if fixed, we use convert function
    game_images["background"]=pygame.image.load(background).convert()
    game_images["flappy"]=pygame.image.load(flappy).convert_alpha()

    game_sounds["death"]=pygame.mixer.Sound('audio/die.wav')
    game_sounds["hit"]=pygame.mixer.Sound('audio/hit.wav')
    game_sounds["points"]=pygame.mixer.Sound('audio/point.wav')
    game_sounds["swoosh"]=pygame.mixer.Sound('audio/swoosh.wav')
    game_sounds["wing"]=pygame.mixer.Sound('audio/wing.wav')

    while True:
        welcome_screen() # Welcome screen
        game_screen() # Main game function
