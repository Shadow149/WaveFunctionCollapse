from Collapse import Square
from PatternRecognision import *
from operator import itemgetter
from PIL import Image
from collections import Counter
from itertools import chain

tile_types = ['S','C','L']

input_modules = [['S','S','S','S','S','S','S'],
                 ['S','S','C','C','C','S','S'],
                 ['S','C','L','L','L','C','S'],
                 ['S','C','L','L','L','C','S'],
                 ['S','C','L','L','L','C','S'],
                 ['S','S','C','C','C','S','S'],
                 ['S','S','S','S','S','S','S']]

w = 15
h = 15
output = [[Square(tile_types,'S',True) for i in range(w)] for j in range(h)]

patterns = pattern_recogision(input_modules)

patterns.append(('C','L','MUST'))
patterns.append(('L','C','MUST'))
patterns.append(('S','C','MUST'))
patterns.append(('C','S','MUST'))

#patterns = [('G','S','DOWN'),('G','G','LEFT'),('G','G','RIGHT'),('L','G','TOP'),('P','L','TOP'),('P','P','LEFT'),('P','P','RIGHT'),('S','P','TOP'),('S','P','DOWN'),('S','P','LEFT'),('S','P','RIGHT'),('S','L','LEFT'),('S','L','RIGHT')]

weights = get_weights_from_modules(input_modules)


def display_map(save = False):
    if save:
        im = Image.new("RGB", (w, h))
        pix = im.load()
        for x in range(w):
            for y in range(h):
                if output[x][y].observed_state == 'S':
                    pix[y,x] = (0,0,255)
                elif output[x][y].observed_state == 'L':
                    pix[y,x] = (0,255,0)
                elif output[x][y].observed_state == 'C':
                    pix[y,x] = (252, 202, 3)
        im.save("test.png", "PNG")

    for row in output:
        print(*row)

def display_visited():
    for i in range(w):
        for j in range(h):
            print(int(output[i][j].propogate_visited),'', end='')
        print('',end='\n')

        #print(*row)

def display_stated():
    for i in range(w):
        for j in range(h):
            print(len(output[i][j].possible_tile_types),'', end='')
        print('',end='\n')

        #print(*row)

def collapse_possible():
    entropies = []
    square_positions = []
    for i in range(len(output)):
        for j in range(len(output[0])):
            #print(i,j)
            #if not output[i][j].observed:
            entropy = output[i][j].calculate_entropy(weights)
            entropies.append(entropy)
            square_positions.append([i,j])
    
    min_entropy_square_index = min(enumerate(entropies), key=itemgetter(1))[0] 

    #print(min_entropy_square_index)
    #print(square_positions[min_entropy_square_index])
    while output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].observed_state in output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].possible_tile_types:
        #print('ok',entropies)
        #print('oof')

        entropies[min_entropy_square_index] = 9999
        min_entropy_square_index = min(enumerate(entropies), key=itemgetter(1))[0]

    #print(min_entropy_square_index)
    #print(square_positions[min_entropy_square_index])
    collapsed_state = output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].collapse(weights)

    output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].observed_state = collapsed_state
    output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].possible_tile_types = [collapsed_state]
    output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].observed = True

    return square_positions[min_entropy_square_index]

def neighbors(x, y):
    n = []
    if y > 0:
        n.append([output[x][y-1],'RIGHT'])
    if y < len(output) - 1:
        n.append([output[x][y+1],'LEFT'])
    if x > 0:
        n.append([output[x-1][y], 'DOWN'])
    if x < len(output[y]) - 1:
        n.append([output[x+1][y], 'TOP'])
    return n

def get_opposite_direction(dir):
    if dir == 'TOP':
        return 'DOWN'
    if dir == 'DOWN':
        return 'TOP' 
    if dir == 'RIGHT':
        return 'LEFT' 
    if dir == 'LEFT':
        return 'RIGHT' 

def propogate(x, y, previous_square, direction):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if (not output[x][y].propogate_visited) or previous_square == None:
        possible_states = []

        square_neighbors = neighbors(x,y)
        for neighbor in square_neighbors:
            temp = []
            for pattern in patterns:
                # pattern : ['s','s','LEFT']
                if pattern[1] == neighbor[0].observed_state:
                    if pattern[2] == get_opposite_direction(neighbor[1]):
                        temp.append(pattern[0])
                    #if not neighbor[0].has_requirement_neighboring:
                    #    if pattern[2] == 'MUST':
                    #        #print('bitch')
                    #        neighbor[0].has_requirement_neighboring = True
                    #        output[x][y].has_requirement_neighboring = True
                    #        temp = pattern[0]
            possible_states.append(temp)
        
        #print(possible_states)
        unique_possible_states = set(tile_types)
        for i in possible_states:
            temp = []
            if len(i) == 0:
                temp = tile_types
            else:
                temp = i
            #print(temp)
            #print(unique_possible_states & set(temp))
            unique_possible_states = unique_possible_states & set(temp)
        unique_possible_states = list(unique_possible_states)


        #print(square_neighbors)

        # if previous_square != None and direction != None:
        #     #print('1')
        #     for pattern in patterns:
        #         #print('2')
        #         if pattern[1] == previous_square.observed_state:
        #             #print('3')
        #             if pattern[2] == direction:
        #                 #print(possible_states)
        #                 possible_states.append(pattern[0])
        #print(unique_possible_states)
        if len(unique_possible_states) == 0:
            unique_possible_states = tile_types

            if output[x][y].observed:
                unique_possible_states = [output[x][y].observed_state]

        #print(possible_states)
        #print(x,y,output[x][y].observed_state,unique_possible_states)

        previous_square = output[x][y]

        output[x][y].possible_tile_types = list(set(unique_possible_states))
        output[x][y].propogate_visited = True

        #display_map()
        #display_stated()
        #input()

        if y > 0:
            propogate(x,y-1,output[x][y],'LEFT')
        if y < len(output) - 1:
            propogate(x,y+1,output[x][y],'RIGHT')
        if x > 0:
            propogate(x-1,y,output[x][y],'TOP')
        if x < len(output[y]) - 1:
            propogate(x+1,y,output[x][y],'DOWN')


#collapsed_position = [9,0]
#
if __name__ == '__main__':
    for i in range((w**2)):
        
        collapsed_position = collapse_possible()
        propogate(collapsed_position[0],collapsed_position[1], None, None)

        display_map()
        print('\n')
        #input()
        #display_stated()
        
        for i in range(len(output)):
            for j in range(len(output[0])):
                output[i][j].propogate_visited = False

    display_map(save=True)