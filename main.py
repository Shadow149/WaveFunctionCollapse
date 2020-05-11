from Collapse import Square
from PatternRecognision import *
from operator import itemgetter
from PIL import Image
from collections import Counter
from itertools import chain

tile_types = ['G','T','P','E','S']

input_modules = [['E','S','P','P','E','S'],
                 ['G','G','G','G','G','G'],
                 ['G','G','T','T','G','G'],
                 ['G','G','T','T','G','G'],
                 ['E','S','P','P','E','S'],
                 ['G','G','G','G','G','G']]

input_modules_weights = [['G','G','G','G'],
                         ['G','T','T','G'],
                         ['G','T','T','G'],
                         ['S','P','P','E'],]

# tile_types = ['LC','BC','RC','TC','L','S']

# input_modules = [['S','S','S','S','S','S','S'],
#                  ['S','S','TC','TC','TC','S','S'],
#                  ['S','LC','L','L','L','RC','S'],
#                  ['S','LC','L','L','L','RC','S'],
#                  ['S','LC','L','L','L','RC','S'],
#                  ['S','S','BC','BC','BC','S','S'],
#                  ['S','S','S','S','S','S','S']]

# input_modules_weights = [['S','TC','TC','TC','S'],
#                          ['LC','L','L','L','RC'],
#                          ['LC','L','L','L','RC'],
#                          ['LC','L','L','L','RC'],
#                          ['S','BC','BC','BC','S'],]

# tile_types = ['L','C','P','S','B']

# input_modules = [['S','S','S','S','S','S'],
#                  ['S','L','S','S','S','S'],
#                  ['P','C','P','B','P','P'],
#                  ['S','L','S','L','S','S'],
#                  ['S','L','S','L','S','S'],
#                  ['S','L','S','L','S','S']]

# input_modules_weights = [['S','L','S','S'],
#                          ['P','C','P','B'],
#                          ['S','L','S','L'],
#                          ['S','L','S','L'],]

w = 5
h = 5
output = [[Square(tile_types) for i in range(w)] for j in range(h)]

patterns = pattern_recogision(input_modules_weights)

# patterns.append(('C','S','MUST'))
# patterns.append(('S','C','MUST'))

# patterns.append(('C','L','MUST'))
# patterns.append(('L','C','MUST'))

# patterns.append(('L','S','NOT'))
# patterns.append(('S','L','NOT'))

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
    loop_time = 0
    while output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].observed_state in output[square_positions[min_entropy_square_index][0]][square_positions[min_entropy_square_index][1]].possible_tile_types:
        #print('ok',entropies)
        #print('oof')
        #TODO fix your shit
        loop_time += 1
        entropies[min_entropy_square_index] = 9999
        min_entropy_square_index = min(enumerate(entropies), key=itemgetter(1))[0]

        if loop_time > (w*h):
            return (0,0)

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
        n.append([output[x-1][y], 'TOP'])
    if x < len(output[y]) - 1:
        n.append([output[x+1][y], 'DOWN'])
    return n


def propogate(x, y, previous_square):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if (not output[x][y].propogate_visited) or previous_square == None:
        possible_states = []
        ban_list = []
        must_list = []

        square_neighbors = neighbors(x,y)
        #print(square_neighbors)
        for neighbor in square_neighbors:
            temp = []
            for pattern in patterns:
                # pattern : ['E','S','LEFT']
                if pattern[1] == neighbor[0].observed_state:
                    if pattern[2] == neighbor[1]:
                        #print(pattern)
                        temp.append(pattern[0])
            possible_states.append(temp)
        
        flattened_possible_states = [item for sublist in possible_states for item in sublist]
        #print('flattened_possible_states',flattened_possible_states)
        unique_possible_states = set(flattened_possible_states)
        for i in possible_states:
           temp = []
           if len(i) == 0:
               temp = output[x][y].tile_set
           else:
               temp = i
           #print('t',temp)
           #print('u+t',unique_possible_states & set(temp))
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
        #print('m',must_list)
        #print('bl',ban_list)
        print('ps',possible_states)
        print(unique_possible_states)
        if len(unique_possible_states) == 0:
            #print(type(possible_states))

            #flattened_possible_states = [item for sublist in possible_states for item in sublist]

            # counter = Counter(flattened_possible_states)
            # most_common = counter.most_common()

            # print(most_common)
            # if most_common[0][1] > 1:
            #     unique_possible_states = [most_common[0][0]]
            # else:
            #unique_possible_states = output[x][y].tile_set
            print('gasp')
            return
            #if output[x][y].observed:
            #    unique_possible_states = [output[x][y].observed_state]

        #print(unique_possible_states)
        #print(x,y,output[x][y].observed_state,unique_possible_states)

        #TODO MUST PATTERNS 

        previous_square = output[x][y]

        if output[x][y].possible_tile_types != list(set(unique_possible_states)):

            output[x][y].possible_tile_types = list(set(unique_possible_states))
            output[x][y].propogate_visited = True

            #display_map()
            #display_stated()
            #input()

            
            if y > 0:
                propogate(x,y-1,output[x][y])
            if y < len(output) - 1:
                propogate(x,y+1,output[x][y])
            if x > 0:
                propogate(x-1,y,output[x][y])
            if x < len(output[y]) - 1:
                propogate(x+1,y,output[x][y])


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