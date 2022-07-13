import pygame 
import time 
import random


pygame.init()

white  = (255, 255, 255)
green  = (0, 200, 0)
red    = (200, 0, 0)
black  = (0,   0,   0)

block = 75
dis_width  = 16
dis_height = 8

dis = pygame.display.set_mode((dis_width*block, dis_height*block))
pygame.display.set_caption('Monkey Game')


font_style = pygame.font.SysFont("bahnschrift", 50)

def message(msg):
    mesg = font_style.render(msg, True, black)
    dis.blit(mesg, [(dis_width*block)/2.5, (dis_height*block)/2-20])

def loss():
    dis.fill(red)
    message("You Lost")
    pygame.display.update()
    time.sleep(1)
    return True

def win():
    dis.fill(green)
    message("You Win")
    pygame.display.update()
    time.sleep(1)
    return True

def create_coord():
    block_x = round(random.randrange(0, dis_width) )*block
    block_y = round(random.randrange(0, dis_height) )*block
    coord = [block_x, block_y]
    return coord

def create_block(level):
    dis.fill(black)
    blocks = {}
    for i in range (0, level):
        coord = create_coord()
        while coord in blocks.values():
            coord = create_coord()
        pygame.draw.rect(dis, white, [coord[0], coord[1], block, block])

        mesg = font_style.render(str(i+1), True, black)
        dis.blit(mesg, [(coord[0]*2 -15 + block)/2, (coord[1]*2)/2])

        blocks[i] = [coord[0], coord[1]] 
        i += 1
    return(blocks)

def play(level):
    game_over = False

    blocks = create_block(level)
    
    while not game_over:
        
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()

                for i in list(blocks.keys()):
                        
                    if x > blocks[i][0] and x < blocks[i][0]+ block and y > blocks[i][1] and y < blocks[i][1] + block:
                        if i == list(blocks.keys())[0]:
                            pygame.draw.rect(dis, black, [blocks[i][0], blocks[i][1], block, block])
                            del blocks[i]
                            if i == 0:
                                for i in list(blocks.keys()):
                                    pygame.draw.rect(dis, white, [blocks[i][0], blocks[i][1], block, block])
                            if list(blocks.keys()) == []:
                                win()
                                play(level+1)
                        else:
                            loss()
                            play(level-1)
    pygame.quit()
    quit()
play(6)
