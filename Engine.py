import pygame
import main

pygame.init()
grid_size = 50
gameDisplay = pygame.display.set_mode((grid_size*main.w,grid_size*main.h))
pygame.display.set_caption('')

crashed = False


squares = []
font = pygame.font.Font('freesansbold.ttf', 8) 

def render():
    for i in range(len(main.output)):
        for j in range(len(main.output[0])):
            main.output[j][i].propogate_visited = False

            r = pygame.Rect(i*grid_size,j*grid_size,grid_size,grid_size)
            if main.output[j][i].observed_state == 'G':
                carImg = pygame.image.load('./texture/grass.png')
                gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
                #pygame.draw.rect(gameDisplay,pygame.Color(135, 219, 83),r)
            elif main.output[j][i].observed_state == 'T':
                carImg = pygame.image.load('./texture/tree.png')
                gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
                #pygame.draw.rect(gameDisplay,pygame.Color(88, 122, 67),r)
            elif main.output[j][i].observed_state == 'P':
                carImg = pygame.image.load('./texture/path.png')
                gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
                #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            elif main.output[j][i].observed_state == 'E':
                carImg = pygame.image.load('./texture/end.png')
                gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
                #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            elif main.output[j][i].observed_state == 'S':
                carImg = pygame.image.load('./texture/start.png')
                gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
                #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            
            # if main.output[j][i].observed_state == 'LC':
            #     carImg = pygame.image.load('./texture/leftcoast.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(135, 219, 83),r)
            # elif main.output[j][i].observed_state == 'RC':
            #     carImg = pygame.image.load('./texture/rightcoast.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(88, 122, 67),r)
            # elif main.output[j][i].observed_state == 'TC':
            #     carImg = pygame.image.load('./texture/topcoast.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            # elif main.output[j][i].observed_state == 'BC':
            #     carImg = pygame.image.load('./texture/bottomcoast.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            # elif main.output[j][i].observed_state == 'S':
            #     carImg = pygame.image.load('./texture/sea.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            # elif main.output[j][i].observed_state == 'L':
            #     carImg = pygame.image.load('./texture/land.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)

            # if main.output[j][i].observed_state == 'C':
            #     carImg = pygame.image.load('./texture/connector.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(135, 219, 83),r)
            # elif main.output[j][i].observed_state == 'B':
            #     carImg = pygame.image.load('./texture/connectorb.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(135, 219, 83),r)
            # elif main.output[j][i].observed_state == 'L':
            #     carImg = pygame.image.load('./texture/ladder.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(88, 122, 67),r)
            # elif main.output[j][i].observed_state == 'P':
            #     carImg = pygame.image.load('./texture/platform.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)
            # elif main.output[j][i].observed_state == 'S':
            #     carImg = pygame.image.load('./texture/sky.png')
            #     gameDisplay.blit(carImg, (i*grid_size,j*grid_size))
            #     #pygame.draw.rect(gameDisplay,pygame.Color(117, 100, 62),r)


            textstring = str(main.output[j][i].observed_state)
            text = font.render(textstring, True, (0,0,0))
            textRect = text.get_rect()  
            
            textRect.center = (int(i*grid_size + (grid_size // 2)), int(j*grid_size + (grid_size // 2))) 
            gameDisplay.blit(text, textRect) 

            textstring = str(main.output[j][i].possible_tile_types)
            text = font.render(textstring, True, (0,0,0))
            textRect = text.get_rect()  
            
            textRect.center = (int(i*grid_size + (grid_size // 2)), int(j*grid_size + (grid_size // 2) + 10)) 
            gameDisplay.blit(text, textRect) 

clicked = False
while not crashed:
        
    clicked = False
    collapsed_position = main.collapse_possible()
    main.propogate(collapsed_position[0],collapsed_position[1], None)
    print(clicked)
    main.display_map()
    print('\n')
    #display_stated()
    
    while not clicked and not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        gameDisplay.fill((0,0,255))

        render()
        
        if pygame.mouse.get_pressed()[0] == 1 and not clicked:
            clicked = True

        pygame.display.update()

    while pygame.mouse.get_pressed()[0] == 1 and not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        gameDisplay.fill((0,0,255))

        render()
        pygame.display.update()

# while not crashed:

#     gameDisplay.fill((0,0,255))
    

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True

#     mouse_pos = pygame.mouse.get_pos()
#     x = mouse_pos[0]
#     y = mouse_pos[1]
#     grid_x = x - (x%grid_size)
#     grid_y = y - (y%grid_size)
#     #print(grid_x/grid_size,grid_y/grid_size)
#     # if pygame.mouse.get_pressed()[0] == 1:
#     #     if main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state == 'S':
#     #         main.display_map()
#     #         r = pygame.Rect(x - (x%grid_size),y - (y%grid_size),grid_size,grid_size)
#     #         squares.append(r)
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed = True
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state = 'L'
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].tile_set = ['L','C']
            
#     #         #collapsed_position = main.collapse_possible()
#     #         main.propogate(int(grid_y/grid_size),int(grid_x/grid_size), None, None, 0)
#     #         print('\n')
#     #         print('\n')
#     #         #main.display_stated()

#     #         probosed_state = main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].collapse(main.weights)
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state = probosed_state
#     #         #print(main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state)

#     #         for square in squares:
#     #             main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state = main.output[int(square.y/grid_size)][int(square.x/grid_size)].collapse(main.weights)
#     #         for i in range(len(main.output)):
#     #             for j in range(len(main.output[0])):
#     #                 main.output[i][j].propogate_visited = False
#     #         #pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),r)
            
#     # if pygame.mouse.get_pressed()[2] == 1:
#     #     if main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state == 'S':
#     #         main.display_map()
#     #         r = pygame.Rect(x - (x%grid_size),y - (y%grid_size),grid_size,grid_size)
#     #         squares.append(r)
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed = True
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state = 'S'
#     #         main.output[int(Srid_y/grid_size)][int(grid_x/grid_size)].tile_set = ['S']
            
#     #         #collapsed_position = main.collapse_possible()
#     #         main.propogate(int(grid_y/grid_size),int(grid_x/grid_size), None, None, 0)
#     #         print('\n')
#     #         print('\n')
#     #         #main.display_stated()

#     #         probosed_state = main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].collapse(main.weights)
#     #         main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state = probosed_state
#     #         #print(main.output[int(grid_y/grid_size)][int(grid_x/grid_size)].observed_state)

#     #         #for square in squares:
#     #         #    main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state = main.output[int(square.y/grid_size)][int(square.x/grid_size)].collapse(main.weights)
#     #         for i in range(len(main.output)):
#     #             for j in range(len(main.output[0])):
#     #                 main.output[i][j].propogate_visited = False
#     #         #pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),r)

    
#     render()
#     # for square in squares:
#     #     if main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state == 'S':
#     #         pygame.draw.rect(gameDisplay,pygame.Color(0,0,255),square)
#     #     elif main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state == 'C':
#     #         pygame.draw.rect(gameDisplay,pygame.Color(240, 224, 84),square)
#     #     elif main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state == 'L':
#     #         pygame.draw.rect(gameDisplay,pygame.Color(85, 207, 99),square)
#     #     elif main.output[int(square.y/grid_size)][int(square.x/grid_size)].observed_state == 'M':
#     #         pygame.draw.rect(gameDisplay,pygame.Color(86, 110, 88),square)

#     #     textstring = str(len(main.output[int(square.y/grid_size)][int(square.x/grid_size)].possible_tile_types)) + str(main.output[int(square.y/grid_size)][int(square.x/grid_size)].possible_tile_types)
#     #     text = font.render(textstring, True, (0,0,0))
#     #     # create a rectangular object for the 
#     #     # text surface object 
#     #     textRect = text.get_rect()  
        
#     #     # set the center of the rectangular object. 
#     #     textRect.center = (int(square.x + (grid_size // 2)), int(square.y + (grid_size // 2))) 
#     #     gameDisplay.blit(text, textRect) 
    
#     rect_surface = pygame.Surface((grid_size,grid_size), pygame.SRCALPHA)   # per-pixel alpha
#     rect_surface.fill((255,255,255,50))
#     gameDisplay.blit(rect_surface,(grid_x,grid_y))
    
#     #r = pygame.Rect(x - (x%grid_size),y - (y%grid_size),grid_size,grid_size)
#     #pygame.draw.rect(gameDisplay,pygame.Color(255,255,255,a=255),r)

#     pygame.display.update()
