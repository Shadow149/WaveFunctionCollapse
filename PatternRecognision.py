from collections import Counter


def get_weights_from_modules(modules: list) -> dict:
    flattened_list = [j for sub in modules for j in sub]
    return dict(Counter(flattened_list))

#get_weights_from_modules(input_modules)

def columns_to_row(aList: list):
    newList = [[ [None] for i in range(len(aList[0])) ] for i in range(len(aList))]

    for y in range(len(aList)):
        for x in range(len(aList[y])):
            newList[y][x] = aList[x][y]

    return newList
            

def pattern_recogision(modules: list):
    patterns = []

    previousModule = None
    for row in modules:
        for module in row:
            if previousModule != None:
                print(previousModule,'<->',module)

                newPattern = (previousModule,module,'LEFT')
                newPatternReverse = (module,previousModule,'RIGHT')
                newPattern1 = (previousModule,module,'RIGHT')
                newPatternReverse1 = (module,previousModule,'LEFT')

                isNewPattern = False
                isNewPatternReverse = False
                isNewPattern1 = False
                isNewPatternReverse1 = False

                for pattern in patterns:
                    if pattern == newPattern:
                        isNewPattern = True
                    if pattern == newPatternReverse:
                        isNewPatternReverse = True
                    if pattern == newPattern1:
                        isNewPattern1 = True
                    if pattern == newPatternReverse1:
                        isNewPatternReverse1 = True

                if not isNewPattern:
                    patterns.append(newPattern)

                if not isNewPatternReverse:
                    patterns.append(newPatternReverse)
                    
                # if not isNewPattern1:
                #     patterns.append(newPattern1)

                # if not isNewPatternReverse:
                #     patterns.append(newPatternReverse1)

            previousModule = module
        previousModule = None

    flipped_modules = columns_to_row(modules)
    print('---------------')

    previousModule = None
    for row in flipped_modules:
        for module in row:
            if previousModule != None:
                print(previousModule,'<->',module)

                newPattern = (previousModule,module,'DOWN')
                newPatternReverse = (module,previousModule,'TOP')
                newPattern1 = (previousModule,module,'TOP')
                newPatternReverse1 = (module,previousModule,'DOWN')

                isNewPattern = False
                isNewPatternReverse = False
                isNewPattern1 = False
                isNewPatternReverse1 = False

                for pattern in patterns:
                    if pattern == newPattern:
                        isNewPattern = True
                    if pattern == newPatternReverse:
                        isNewPatternReverse = True
                    if pattern == newPattern1:
                        isNewPattern1 = True
                    if pattern == newPatternReverse1:
                        isNewPatternReverse1 = True

                if not isNewPattern:
                    patterns.append(newPattern)

                if not isNewPatternReverse:
                    patterns.append(newPatternReverse)

                # if not isNewPattern1:
                #     patterns.append(newPattern1)

                # if not isNewPatternReverse1:
                #     patterns.append(newPatternReverse1)

            previousModule = module
        previousModule = None


    
    print(patterns)
    print(len(patterns))
    return patterns

if __name__ == '__main__':
    pattern_recogision(input_modules)
