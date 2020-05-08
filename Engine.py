import pygame
import main

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')

crashed = False

grid_size = 50

squares = []

while not crashed:

    gameDisplay.fill((0,0,0))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    mouse_pos = pygame.mouse.get_pos()
    x = mouse_pos[0]
    y = mouse_pos[1]
    grid_x = x - (x%grid_size)
    grid_y = y - (y%grid_size)
    print(grid_x/grid_size,grid_y/grid_size)
    
    if pygame.mouse.get_pressed()[0] == 1:
        r = pygame.Rect(x - (x%grid_size),y - (y%grid_size),grid_size,grid_size)
        squares.append(r)
        main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed = True
        main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state = 'L'
        
        collapsed_position = main.collapse_possible()
        #main.propogate(int(grid_y/grid_size),int(grid_x/grid_size), None, None)
        main.display_map()
        #pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),r)
        
    for square in squares:
        pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),square)
    
    rect_surface = pygame.Surface((grid_size,grid_size), pygame.SRCALPHA)   # per-pixel alpha
    rect_surface.fill((255,255,255,50))
    gameDisplay.blit(rect_surface,(grid_x,grid_y))
    
    #r = pygame.Rect(x - (x%grid_size),y - (y%grid_size),grid_size,grid_size)
    #pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),r)

    pygame.display.update()
